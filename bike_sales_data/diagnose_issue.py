"""
Diagnostic script to identify database loading issues
"""

import os
import sys
import pandas as pd
from pathlib import Path

print("=" * 80)
print("DIAGNOSTIC: Database Loading Issues")
print("=" * 80)

# Check current working directory
print(f"\n1. Current Working Directory:")
print(f"   {os.getcwd()}")

# Check if CSV files exist
print(f"\n2. CSV Files in Current Directory:")
csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
if csv_files:
    for f in csv_files:
        print(f"   ✓ {f}")
        try:
            df = pd.read_csv(f)
            print(f"      → Loaded: {len(df)} rows, {len(df.columns)} columns")
        except Exception as e:
            print(f"      → ERROR loading: {e}")
else:
    print("   ❌ NO CSV FILES FOUND")

# Check absolute paths
print(f"\n3. Absolute Path Check:")
script_dir = Path(__file__).parent
print(f"   Script location: {script_dir}")

for csv_file in ['bike_sales_numeric_sp.csv', 'ipl_dataset_10000.csv']:
    full_path = script_dir / csv_file
    print(f"\n   {csv_file}:")
    print(f"      Path: {full_path}")
    print(f"      Exists: {full_path.exists()}")
    if full_path.exists():
        try:
            df = pd.read_csv(str(full_path))
            print(f"      Status: ✓ Loaded ({len(df)} rows, {len(df.columns)} columns)")
        except Exception as e:
            print(f"      Status: ❌ ERROR: {e}")

# Test the actual loader
print(f"\n4. Testing GenericDataLoader:")
try:
    from generic_data_loader import GenericDataLoader
    print("   ✓ Module imported successfully")
    
    # Try loading
    try:
        loader = GenericDataLoader('bike_sales_numeric_sp.csv')
        print(f"   ✓ Loader initialized with bike_sales_numeric_sp.csv")
        print(f"      Records: {len(loader.df)}")
        print(f"      Columns: {len(loader.df.columns)}")
        print(f"      Entity Column: {loader.entity_column}")
    except Exception as e:
        print(f"   ❌ Error initializing loader: {e}")
        import traceback
        traceback.print_exc()
        
except ImportError as e:
    print(f"   ❌ Error importing module: {e}")

print("\n" + "=" * 80)
