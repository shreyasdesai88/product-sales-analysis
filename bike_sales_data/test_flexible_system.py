"""
Test Script - Demonstrates flexible analytics with different datasets
"""

from generic_data_loader import GenericDataLoader
from flexible_analytics_engine import FlexibleAnalyticsEngine
from dynamic_visualizer import DynamicVisualizer


def test_dataset(csv_file):
    """Test and demonstrate analysis for a dataset"""
    
    print("\n" + "="*80)
    print(f"TESTING: {csv_file}")
    print("="*80)
    
    try:
        # Load data
        print("\n📥 Loading data...")
        loader = GenericDataLoader(csv_file)
        
        # Initialize analytics
        print("\n🔧 Initializing analytics...")
        analytics = FlexibleAnalyticsEngine(loader)
        
        # Initialize visualizer
        print("\n🎨 Initializing visualizer...")
        visualizer = DynamicVisualizer(loader, analytics)
        
        # Get entities
        entities = loader.get_all_entities()
        print(f"\n✓ Found {len(entities)} entities")
        print(f"  Entity column: {loader.entity_column}")
        print(f"  Entities: {entities[:5]}{'...' if len(entities) > 5 else ''}")
        
        # Show metrics
        print(f"\n📊 Available metrics ({len(loader.numeric_columns)}):")
        for col in loader.numeric_columns[:5]:
            print(f"  • {col}")
        if len(loader.numeric_columns) > 5:
            print(f"  ... and {len(loader.numeric_columns) - 5} more")
        
        # Show categories
        print(f"\n📂 Available categories ({len(loader.categorical_columns)}):")
        for col in loader.categorical_columns[:5]:
            print(f"  • {col}")
        
        # Show date columns
        print(f"\n📅 Date columns ({len(loader.date_columns)}):")
        for col in loader.date_columns:
            print(f"  • {col}")
        
        # Perform comparison
        if len(entities) >= 2:
            print(f"\n🔄 Comparing: {entities[0]} vs {entities[1]}")
            print(analytics.get_comparison_summary(entities[0], entities[1]))
            
            # Generate insights
            print("\n💡 Insights:")
            insights = analytics.generate_insights(entities[0], entities[1])
            for insight in insights:
                print(f"  {insight}")
        
        # Available charts
        print("\n📈 Available chart types:")
        charts = visualizer.get_available_chart_types()
        for chart_cat, chart_list in charts.items():
            print(f"  {chart_cat}: {', '.join(chart_list)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("\n" + "="*80)
    print("FLEXIBLE ANALYTICS ENGINE - MULTI-DATASET TEST")
    print("="*80)
    
    # Test with bike sales
    test_dataset('bike_sales_numeric_sp.csv')
    
    # Test with IPL
    test_dataset('ipl_dataset_10000.csv')
    
    print("\n" + "="*80)
    print("✓ ALL TESTS COMPLETED")
    print("="*80)
    print("\n🚀 NEXT STEPS:")
    print("  1. Run the dynamic dashboard:")
    print("     streamlit run dynamic_dashboard.py")
    print("\n  2. Switch between datasets easily in the sidebar")
    print("\n  3. Dashboard automatically adapts to any CSV structure!")
    print("\n" + "="*80)
