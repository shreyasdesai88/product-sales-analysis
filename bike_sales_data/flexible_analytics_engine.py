"""
Flexible Analytics Engine - Works with ANY dataset
Auto-generates KPIs and comparisons based on available columns
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from generic_data_loader import GenericDataLoader


class FlexibleAnalyticsEngine:
    """Universal analytics engine that adapts to any dataset structure"""
    
    def __init__(self, loader: GenericDataLoader):
        """Initialize with a GenericDataLoader instance"""
        self.loader = loader
        self.df = loader.df
        self.entity_column = loader.entity_column
        self.numeric_columns = loader.numeric_columns
        self.categorical_columns = loader.categorical_columns
        self.date_columns = loader.date_columns
    
    def compare_entities(self, entity1: str, entity2: str, date_col=None) -> Dict[str, Any]:
        """
        Compare two entities (teams, products, etc.) across all metrics
        
        Args:
            entity1: First entity name
            entity2: Second entity name
            date_col: Optional date column for time-based filtering
        
        Returns:
            Dictionary with comprehensive comparison
        """
        if not self.entity_column:
            return {'error': 'No entity column detected'}
        
        # Get data for both entities
        data1 = self.loader.get_entity_data(entity1)
        data2 = self.loader.get_entity_data(entity2)
        
        comparison = {
            'entity1': entity1,
            'entity2': entity2,
            'records': {entity1: len(data1), entity2: len(data2)},
            'metrics': {}
        }
        
        # Calculate metrics for numeric columns
        for col in self.numeric_columns:
            comparison['metrics'][col] = {
                entity1: self._calculate_metric_stats(data1[col]),
                entity2: self._calculate_metric_stats(data2[col]),
                'difference': self._calculate_metric_stats(data1[col])['sum'] - 
                             self._calculate_metric_stats(data2[col])['sum']
            }
        
        # Get categorical distributions
        comparison['categorical'] = {}
        for col in self.categorical_columns:
            if col != self.entity_column:  # Skip entity column itself
                comparison['categorical'][col] = {
                    entity1: data1[col].value_counts().to_dict(),
                    entity2: data2[col].value_counts().to_dict()
                }
        
        return comparison
    
    def _calculate_metric_stats(self, series: pd.Series) -> Dict[str, float]:
        """Calculate statistics for a metric"""
        series_clean = pd.to_numeric(series, errors='coerce').dropna()
        
        return {
            'sum': series_clean.sum(),
            'mean': series_clean.mean(),
            'median': series_clean.median(),
            'min': series_clean.min(),
            'max': series_clean.max(),
            'std': series_clean.std(),
            'count': len(series_clean)
        }
    
    def get_entity_aggregates(self, entity_name: str) -> Dict[str, Any]:
        """Get aggregated metrics for a single entity"""
        data = self.loader.get_entity_data(entity_name)
        
        aggregates = {}
        for col in self.numeric_columns:
            aggregates[col] = self._calculate_metric_stats(data[col])
        
        return aggregates
    
    def get_time_series(self, entity_name: str = None, 
                       metric_col: str = None, 
                       date_col: str = None,
                       frequency: str = 'D') -> pd.DataFrame:
        """
        Get time series data for a metric
        
        Args:
            entity_name: Filter by entity (optional)
            metric_col: Column to aggregate (first numeric if None)
            date_col: Date column to use (first datetime if None)
            frequency: 'D' (daily), 'W' (weekly), 'M' (monthly), 'Y' (yearly)
        """
        if not self.date_columns:
            return pd.DataFrame()
        
        data = self.df.copy()
        if entity_name and self.entity_column:
            data = data[data[self.entity_column] == entity_name]
        
        if metric_col is None and self.numeric_columns:
            metric_col = self.numeric_columns[0]
        
        if date_col is None:
            date_col = self.date_columns[0]
        
        if metric_col and date_col:
            data[date_col] = pd.to_datetime(data[date_col])
            ts = data.groupby(pd.Grouper(key=date_col, freq=frequency))[metric_col].agg(['sum', 'mean', 'count'])
            return ts
        
        return pd.DataFrame()
    
    def get_top_performers(self, metric_col: str = None, 
                          top_n: int = 5,
                          categorical_col: str = None) -> Dict[str, Any]:
        """
        Get top performing entities or categories
        
        Args:
            metric_col: Column to rank by (first numeric if None)
            top_n: Number of top performers
            categorical_col: Column to group by (first categorical if None)
        """
        if metric_col is None and self.numeric_columns:
            metric_col = self.numeric_columns[0]
        
        if categorical_col is None and self.categorical_columns:
            categorical_col = self.categorical_columns[0]
        
        if not metric_col or not categorical_col:
            return {}
        
        top_data = self.df.groupby(categorical_col)[metric_col].sum().nlargest(top_n)
        return {
            'metric': metric_col,
            'groupby': categorical_col,
            'data': top_data.to_dict()
        }
    
    def get_comparison_summary(self, entity1: str, entity2: str) -> str:
        """Generate a text summary of comparison"""
        comparison = self.compare_entities(entity1, entity2)
        
        summary = f"\n{'='*60}\n"
        summary += f"COMPARISON: {entity1} vs {entity2}\n"
        summary += f"{'='*60}\n"
        
        summary += f"\nRecords: {comparison['records'][entity1]} vs {comparison['records'][entity2]}\n"
        
        summary += f"\n💰 METRICS:\n"
        for metric, values in comparison['metrics'].items():
            e1_sum = values[entity1]['sum']
            e2_sum = values[entity2]['sum']
            diff = values['difference']
            summary += f"  {metric}:\n"
            summary += f"    {entity1}: {e1_sum:,.2f}\n"
            summary += f"    {entity2}: {e2_sum:,.2f}\n"
            summary += f"    Difference: {diff:,.2f}\n"
        
        if comparison['categorical']:
            summary += f"\n📊 CATEGORICAL DATA:\n"
            for col, data in comparison['categorical'].items():
                summary += f"  {col}:\n"
                summary += f"    {entity1}: {len(data[entity1])} categories\n"
                summary += f"    {entity2}: {len(data[entity2])} categories\n"
        
        return summary
    
    def get_correlation_analysis(self, entity_name: str = None) -> pd.DataFrame:
        """Get correlation matrix for numeric columns"""
        data = self.df.copy()
        if entity_name and self.entity_column:
            data = data[data[self.entity_column] == entity_name]
        
        numeric_data = data[self.numeric_columns]
        return numeric_data.corr()
    
    def generate_insights(self, entity1: str, entity2: str) -> List[str]:
        """Generate actionable insights from comparison"""
        comparison = self.compare_entities(entity1, entity2)
        insights = []
        
        # Analyze metrics
        for metric, values in comparison['metrics'].items():
            e1_val = values[entity1]['sum']
            e2_val = values[entity2]['sum']
            
            if e1_val > e2_val * 1.1:
                pct = ((e1_val - e2_val) / e2_val * 100)
                insights.append(f"✓ {entity1} leads in {metric} by {pct:.1f}%")
            elif e2_val > e1_val * 1.1:
                pct = ((e2_val - e1_val) / e1_val * 100)
                insights.append(f"✓ {entity2} leads in {metric} by {pct:.1f}%")
        
        return insights


if __name__ == "__main__":
    # Test with bike sales
    print("=" * 80)
    print("FLEXIBLE ANALYTICS ENGINE - BIKE SALES TEST")
    print("=" * 80)
    
    loader_bike = GenericDataLoader('bike_sales_numeric_sp.csv')
    analytics_bike = FlexibleAnalyticsEngine(loader_bike)
    
    entities = analytics_bike.loader.get_all_entities()
    if len(entities) >= 2:
        print(analytics_bike.get_comparison_summary(entities[0], entities[1]))
        print("\nInsights:")
        for insight in analytics_bike.generate_insights(entities[0], entities[1]):
            print(f"  {insight}")
    
    # Test with IPL
    print("\n" + "=" * 80)
    print("FLEXIBLE ANALYTICS ENGINE - IPL TEST")
    print("=" * 80)
    
    loader_ipl = GenericDataLoader('ipl_dataset_10000.csv')
    analytics_ipl = FlexibleAnalyticsEngine(loader_ipl)
    
    entities = analytics_ipl.loader.get_all_entities()
    if len(entities) >= 2:
        print(analytics_ipl.get_comparison_summary(entities[0], entities[1]))
        print("\nInsights:")
        for insight in analytics_ipl.generate_insights(entities[0], entities[1]):
            print(f"  {insight}")
