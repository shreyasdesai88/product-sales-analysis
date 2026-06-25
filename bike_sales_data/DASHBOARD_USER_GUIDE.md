# 📊 Dashboard Enhancements - User Guide

## New Features

The Flexible Comparison Dashboard now includes two major enhancements:

### 1. **📤 File Upload Capability**
Users can now upload their own CSV datasets directly to the dashboard without needing to place them in the project directory.

### 2. **🎯 KPI Selection**
Users can select which KPIs (Key Performance Indicators) they want to analyze and display in all tabs.

---

## How to Use

### Starting the Dashboard

```bash
streamlit run dynamic_dashboard.py
```

The dashboard will open at: `http://localhost:8501`

---

## Feature 1: Dataset Configuration

The sidebar has two tabs for dataset selection:

#### **Option A: Upload Your Own CSV File** 📤

1. Click the **"Upload Dataset"** tab in the sidebar
2. Click **"Choose a CSV file"**
3. Select a CSV file from your computer
4. The file will be automatically loaded and analyzed
5. See the dataset info in the **"Dataset Info"** expander

**Requirements:**
- CSV file format
- At least 1 column with 2+ unique values (entity)
- At least 1 numeric column (metric)

**Example datasets:**
- Sales data with product/store columns
- Sports data with team columns
- Performance metrics with category columns
- Any data with entities to compare

#### **Option B: Use Local Files** 📁

1. Click the **"Local Files"** tab in the sidebar
2. Select from the dropdown list of CSV files in the project directory
3. The selected file will be analyzed automatically

**Available local files:**
- `bike_sales_numeric_sp.csv` - Bike sales data (6 products)
- `ipl_dataset_10000.csv` - IPL cricket data (2 teams)

---

## Feature 2: KPI Selection

### What are KPIs?

KPIs are numeric metrics/columns from your dataset that you want to analyze:
- Price, Revenue, Sales (business)
- Runs, Wickets, Overs (sports)
- Performance scores, metrics (analytics)

### How to Select KPIs

1. **In the Sidebar**, find the **"KPI Selection"** section
2. **Multi-select** the metrics you want to display:
   - Click checkboxes to select individual KPIs
   - Or use "Select all" / "Deselect all"
3. **Selected KPIs** appear in real-time in:
   - Comparison tab (metrics table)
   - Charts tab (bar charts)
   - Metrics tab (detailed statistics)
   - Trends tab (time series)

### Example: Bike Sales Dashboard

**Available KPIs:**
- Sale_ID
- Customer_ID
- Price
- Quantity
- Salesperson_ID
- Customer_Age
- Total_Sales

**You select:** Price, Quantity, Total_Sales

**Result:** Only these 3 metrics appear in all analyses and visualizations

---

## Dashboard Workflow

### Step 1️⃣: Upload or Select Dataset
```
📊 Dataset Configuration
  📤 Upload Dataset (or)
  📁 Local Files
```

### Step 2️⃣: Select KPIs to Display
```
🎯 KPI Selection
  ☑ Price
  ☑ Quantity
  ☑ Total_Sales
  ☐ Sale_ID
  ...
```

### Step 3️⃣: Choose Entities to Compare
```
Entity 1: Himalayan 450
Entity 2: KTM 390 Adventure
```

### Step 4️⃣: View Analysis
- **📊 Comparison** - Side-by-side metrics table with selected KPIs
- **📈 Charts** - Bar charts comparing selected KPIs
- **🔍 Metrics** - Detailed statistics (sum, mean, median, etc.) for each selected KPI
- **📅 Trends** - Time series analysis for selected KPIs
- **🎯 Insights** - Key findings between the two entities

---

## Comparison Tab Example

```
💰 KPI Comparison (Selected Metrics)

| Metric      | Bike Model A | Bike Model B | Difference |
|-------------|--------------|-------------|-----------|
| Price       | 531,270,346  | 530,212,653 | 1,057,693 |
| Quantity    | 2,313        | 2,341       | -28       |
| Total_Sales | 660,105,829  | 667,046,028 | -6,940,199|

(Only selected KPIs are shown)
```

---

## Charts Tab Example

### Metric Comparison
```
Select Metrics to Display
☑ Price
☑ Quantity
☑ Total_Sales

[Bar Chart showing these 3 metrics only]
```

---

## Metrics Tab Example

### Detailed Statistics

Only selected KPIs are available in the dropdown:

```
Select Metric: [Price ▼]

Chennai Super Kings          |  Mumbai Indians
---------------------------- | ----------------------------
Sum: 848,623                 | Sum: 843,576
Mean: 169                    | Mean: 169
Median: 169                  | Median: 169
Min: 50                      | Min: 45
Max: 290                     | Max: 295
Std Dev: 45.23               | Std Dev: 46.12
Count: 5,021                 | Count: 4,979
```

---

## Tips & Best Practices

### ✅ Do:
- **Start with 3-5 KPIs** for focused analysis
- **Use descriptive KPI names** like "Revenue", "Units_Sold"
- **Compare similar metrics** (don't mix units)
- **Check Dataset Info** to understand your data structure

### ❌ Don't:
- **Select too many KPIs** (hard to visualize)
- **Use ID columns** as KPIs (they're sums, not meaningful)
- **Compare unrelated metrics** (e.g., price with count)
- **Forget to select at least 1 KPI** (needed for analysis)

---

## Upload Dataset Format

Your CSV file should have this structure:

```csv
entity_column,metric1,metric2,category1,date_column
Value1,100,50,CategoryA,2023-01-01
Value2,120,45,CategoryB,2023-01-02
Value3,95,60,CategoryA,2023-01-03
```

**Required:**
- `entity_column`: Column with 2+ unique values (teams, products, etc.)
- At least 1 numeric column for metrics
- Date column is optional (for trends tab)
- Categories are optional (for categorical analysis)

**Example Real Data:**

Bike Sales:
```
Bike_Model,Price,Quantity,Total_Sales,Store_Location,Date
Himalayan 450,100000,50,5000000,Mumbai,2023-01-01
KTM 390,80000,75,6000000,Delhi,2023-01-01
```

Sports:
```
team,runs_scored,wickets_lost,opponent,venue,match_date
CSK,150,8,MI,Wankhede,2023-04-01
MI,165,6,CSK,Chepauk,2023-04-02
```

---

## Troubleshooting

### Issue: "No CSV files found"
**Solution:** Upload a CSV file using the "Upload Dataset" tab

### Issue: "Need at least 2 entities to compare"
**Solution:** Your dataset needs a column with 2+ unique values. The system auto-detects this - if it fails, your data might need the entity column to be first or have clear categorical values

### Issue: "No selected KPIs found"
**Solution:** Go to KPI Selection in the sidebar and select at least one metric

### Issue: Empty charts or statistics
**Solution:** 
- Make sure you selected the same KPI in both tabs
- Verify your data has numeric values in the KPI columns

### Issue: Upload fails
**Solution:**
- Ensure file is in CSV format
- Check file size (should be < 100MB)
- Verify file contains valid data

---

## Data Auto-Detection

The dashboard automatically detects:

✅ **Entity Columns** - Column with multiple unique values (products, teams, etc.)
✅ **Numeric Columns** - Columns with numbers (your KPIs)
✅ **Categorical Columns** - Columns with categories for analysis
✅ **Date Columns** - Columns with dates for time series

No manual configuration needed!

---

## Advanced: Using Both Features Together

### Example Workflow:

1. **Upload** your custom sales dataset (sales_data.csv)
2. **Select KPIs**: Revenue, Units_Sold, Customer_Count
3. **Compare** Product_A vs Product_B
4. **Analyze**:
   - See side-by-side metrics for your 3 KPIs
   - View trend lines for each KPI over time
   - Examine detailed statistics
   - Get actionable insights

### Result:
Focused analysis on exactly the metrics that matter to you!

---

## Dataset Requirements Summary

| Requirement | Description | Example |
|-------------|-------------|---------|
| Format | CSV file | data.csv |
| Rows | 2+ records | 100, 1000, 10000 |
| Entity Column | 2+ unique values | teams: CSK, MI |
| Numeric Columns | At least 1 | Price, Revenue, Runs |
| Optional Date | For trends analysis | 2023-01-01 |
| Optional Categories | For categorical analysis | Store, Region |

---

## Next Steps

1. **Try uploading a test file** to understand the format
2. **Select different KPI combinations** to focus your analysis
3. **Switch between local and uploaded files** to compare different datasets
4. **Use the Insights tab** to get automated findings

---

**Need help?** Run the demo:
```bash
python demo_ipl_comparison.py
python test_flexible_system.py
```

These show examples of how the system analyzes different data types!

