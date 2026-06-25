"""
Generic Data Loader - Works with ANY dataset
Auto-detects column types and entity relationships
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

class GenericDataLoader:
    """Universal data loader that adapts to any dataset structure"""
    
    def __init__(self, csv_path, entity_column=None):
        """
        Initialize with CSV file path
        
        Args:
            csv_path: Path to CSV file (absolute or relative)
            entity_column: Column name for main entities (e.g., 'team', 'Bike_Model')
                          If None, auto-detects
        """
        self.csv_path = Path(csv_path)
        
        # Ensure path exists
        if not self.csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")
        
        self.df = None
        self.entity_column = entity_column
        self.numeric_columns = []
        self.categorical_columns = []
        self.date_columns = []
        self.column_types = {}
        
        self.load_data()
        self._detect_column_types()
    
    def load_data(self):
        """Load CSV and initial processing"""
        try:
            self.df = pd.read_csv(str(self.csv_path))
            print(f"✓ Data loaded: {len(self.df)} records, {len(self.df.columns)} columns")
            print(f"  Columns: {', '.join(self.df.columns.tolist())}")
            return self.df
        except Exception as e:
            print(f"❌ Error loading CSV: {e}")
            raise
    
    def _detect_column_types(self):
        """Auto-detect column types (numeric, categorical, datetime)"""
        for col in self.df.columns:
            col_data = self.df[col]
            
            # Check if datetime
            if 'date' in col.lower() or 'time' in col.lower():
                try:
                    self.df[col] = pd.to_datetime(col_data)
                    self.date_columns.append(col)
                    self.column_types[col] = 'datetime'
                    continue
                except:
                    pass
            
            # Check if numeric
            if pd.api.types.is_numeric_dtype(col_data):
                self.numeric_columns.append(col)
                self.column_types[col] = 'numeric'
            else:
                # Check if should be numeric (e.g., "100" stored as string)
                try:
                    pd.to_numeric(col_data)
                    self.df[col] = pd.to_numeric(col_data)
                    self.numeric_columns.append(col)
                    self.column_types[col] = 'numeric'
                except:
                    self.categorical_columns.append(col)
                    self.column_types[col] = 'categorical'
        
        # Auto-detect entity column if not provided
        if not self.entity_column:
            self._auto_detect_entity_column()
        
        print(f"\n✓ Column types detected:")
        print(f"  Numeric ({len(self.numeric_columns)}): {self.numeric_columns[:5]}")
        print(f"  Categorical ({len(self.categorical_columns)}): {self.categorical_columns[:5]}")
        print(f"  DateTime ({len(self.date_columns)}): {self.date_columns}")
        if self.entity_column:
            print(f"  Entity Column: {self.entity_column}")
    
    def _auto_detect_entity_column(self):
        """Find the main entity column (team, bike_model, product, etc.)"""
        # Look for columns with moderate cardinality (2-100 unique values)
        cardinality = {}
        for col in self.categorical_columns:
            unique_count = self.df[col].nunique()
            if 2 <= unique_count <= 100:
                cardinality[col] = unique_count
        
        if cardinality:
            # Prefer columns with names suggesting entities
            priority_keywords = ['team', 'product', 'model', 'category', 'type', 'name']
            for keyword in priority_keywords:
                for col, count in cardinality.items():
                    if keyword in col.lower():
                        self.entity_column = col
                        print(f"\n✓ Auto-detected entity column: '{col}'")
                        return
            
            # Otherwise pick the one with lowest cardinality (most grouping)
            self.entity_column = min(cardinality, key=cardinality.get)
            print(f"\n✓ Auto-detected entity column: '{self.entity_column}'")
    
    def get_all_entities(self) -> List[str]:
        """Get list of unique entities (teams, products, etc.)"""
        if not self.entity_column:
            return []
        return sorted(self.df[self.entity_column].unique().tolist())
    
    def get_entity_data(self, entity_name: str) -> pd.DataFrame:
        """Get all data for a specific entity"""
        if not self.entity_column:
            return self.df.copy()
        return self.df[self.df[self.entity_column] == entity_name].copy()
    
    def get_numeric_columns(self) -> List[str]:
        """Get all numeric columns (metrics)"""
        return self.numeric_columns
    
    def get_categorical_columns(self) -> List[str]:
        """Get all categorical columns"""
        return self.categorical_columns
    
    def get_date_columns(self) -> List[str]:
        """Get all datetime columns"""
        return self.date_columns
    
    def get_date_range(self) -> Dict:
        """Get min and max dates across all date columns"""
        if not self.date_columns:
            return {'min_date': None, 'max_date': None}
        
        all_dates = []
        for col in self.date_columns:
            all_dates.extend(self.df[col].dropna())
        
        return {
            'min_date': min(all_dates),
            'max_date': max(all_dates)
        }
    
    def filter_by_date_range(self, start_date, end_date, date_column=None) -> pd.DataFrame:
        """Filter data by date range"""
        if not self.date_columns:
            return self.df.copy()
        
        if date_column is None:
            date_column = self.date_columns[0]
        
        mask = (self.df[date_column] >= start_date) & (self.df[date_column] <= end_date)
        return self.df[mask].copy()
    
    def get_summary_stats(self) -> Dict:
        """Get summary statistics for the dataset"""
        return {
            'total_records': len(self.df),
            'total_columns': len(self.df.columns),
            'entities': self.get_all_entities() if self.entity_column else [],
            'numeric_columns': self.numeric_columns,
            'categorical_columns': self.categorical_columns,
            'date_columns': self.date_columns,
            'date_range': self.get_date_range(),
            'entity_column': self.entity_column,
            'column_types': self.column_types
        }
    
    def get_available_metrics(self) -> Dict[str, List]:
        """Get available metrics grouped by type"""
        return {
            'numeric_metrics': self.numeric_columns,
            'categorical_attributes': self.categorical_columns,
            'time_dimensions': self.date_columns
        }


if __name__ == "__main__":
    # Test with bike sales data
    print("=" * 80)
    print("Testing with Bike Sales Data")
    print("=" * 80)
    
    loader_bike = GenericDataLoader('bike_sales_numeric_sp.csv')
    print(f"\nEntities: {loader_bike.get_all_entities()}")
    print(f"Summary: {loader_bike.get_summary_stats()}")
    
    # Test with IPL data
    print("\n" + "=" * 80)
    print("Testing with IPL Data")
    print("=" * 80)
    
    loader_ipl = GenericDataLoader('ipl_dataset_10000.csv')
    print(f"\nEntities: {loader_ipl.get_all_entities()}")
    print(f"Summary: {loader_ipl.get_summary_stats()}")
