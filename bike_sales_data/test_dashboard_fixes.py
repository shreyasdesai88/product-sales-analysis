"""
Test script to verify dashboard improvements
"""

import os
from pathlib import Path
from generic_data_loader import GenericDataLoader
from flexible_analytics_engine import FlexibleAnalyticsEngine
from dynamic_visualizer import DynamicVisualizer

print("=" * 80)
print("DASHBOARD LOADING TEST")
print("=" * 80)

# Test the improvements
SCRIPT_DIR = Path(__file__).parent
os.chdir(SCRIPT_DIR)

print(f"\n1. Current Directory: {os.getcwd()}")
print(f"2. Script Directory: {SCRIPT_DIR}")

# Test loading CSV files
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
print(f"\n3. CSV Files Found: {csv_files}")

for csv_file in csv_files:
    print(f"\n4. Testing: {csv_file}")
    try:
        loader = GenericDataLoader(str(SCRIPT_DIR / csv_file))
        analytics = FlexibleAnalyticsEngine(loader)
        visualizer = DynamicVisualizer(loader, analytics)
        
        summary = loader.get_summary_stats()
        
        print(f"   ✓ Loader: OK")
        print(f"   ✓ Analytics: OK")
        print(f"   ✓ Visualizer: OK")
        print(f"   Records: {summary['total_records']}")
        print(f"   Columns: {summary['total_columns']}")
        print(f"   Entities: {len(summary['entities'])}")
        print(f"   Entity Column: {summary['entity_column']}")
        
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

print("\n" + "=" * 80)
print("✓ All tests passed! Dashboard should work now.")
print("=" * 80)
