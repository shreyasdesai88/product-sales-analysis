# 🔄 Flexible Dataset Comparison System

## Overview

This project provides a **fully flexible, dataset-agnostic comparison dashboard** that automatically adapts to ANY CSV dataset structure without requiring configuration or code changes.

### Key Features

✅ **Auto-Detection** - Automatically detects:
- Entity columns (teams, products, models, etc.)
- Numeric metrics
- Categorical attributes  
- DateTime columns

✅ **Zero Configuration** - Just add a CSV file, the system handles the rest

✅ **Works with Any Dataset** - Tested with:
- Bike Sales Data (6 products, 10,000 records)
- IPL Cricket Data (2 teams, 10,000 records)
- Any other CSV dataset

✅ **Dynamic Dashboard** - Streamlit app that automatically generates:
- Comparison charts
- KPI metrics
- Time series analysis
- Category distributions
- Correlation matrices
- Insights & trends

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FLEXIBLE SYSTEM MODULES                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. generic_data_loader.py                                  │
│     └─ Auto-detects entity columns & column types           │
│     └─ Handles any CSV structure                            │
│     └─ Exposes: get_all_entities(), get_numeric_columns()   │
│                                                              │
│  2. flexible_analytics_engine.py                            │
│     └─ Universal comparison & aggregation                   │
│     └─ Auto-generates KPIs from available columns           │
│     └─ Provides: compare_entities(), generate_insights()    │
│                                                              │
│  3. dynamic_visualizer.py                                   │
│     └─ Auto-creates charts based on data types              │
│     └─ Generates: bar, line, pie, scatter, heatmap, etc.    │
│                                                              │
│  4. dynamic_dashboard.py (Streamlit App)                    │
│     └─ Interactive UI that auto-adapts to dataset           │
│     └─ Dataset selector in sidebar                          │
│     └─ 5 dynamic tabs with analysis                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## How It Works

### 1. **Data Loading (Generic Data Loader)**

```python
from generic_data_loader import GenericDataLoader

# Load any CSV - system auto-detects structure
loader = GenericDataLoader('ipl_dataset_10000.csv')

# Automatically detected:
loader.entity_column          # → 'team'
loader.numeric_columns        # → ['runs_scored', 'wickets_lost', 'overs_played']
loader.categorical_columns    # → ['opponent', 'venue', 'result', 'player_of_match']
loader.date_columns          # → ['match_date']
loader.get_all_entities()    # → ['Chennai Super Kings', 'Mumbai Indians']
```

### 2. **Analysis (Flexible Analytics Engine)**

```python
from flexible_analytics_engine import FlexibleAnalyticsEngine

analytics = FlexibleAnalyticsEngine(loader)

# Automatic comparison across all metrics
comparison = analytics.compare_entities('Chennai Super Kings', 'Mumbai Indians')

# Returns comparison of ALL numeric columns
# + categorical distributions
# + time series data
# + calculated insights
```

### 3. **Visualization (Dynamic Visualizer)**

```python
from dynamic_visualizer import DynamicVisualizer

visualizer = DynamicVisualizer(loader, analytics)

# Auto-generates appropriate chart types
visualizer.plot_metric_comparison(entity1, entity2)      # Bar chart
visualizer.plot_category_distribution(category_col)      # Pie chart
visualizer.plot_time_series(metric_col)                 # Line chart
visualizer.plot_correlation_heatmap()                   # Heatmap
```

### 4. **Interactive Dashboard (Streamlit)**

The dashboard automatically:
- Detects all CSV files in the folder
- Allows easy switching between datasets
- Adapts all tabs and charts to selected dataset
- Shows entity-specific analysis

## Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run Tests (Optional)

```bash
python test_flexible_system.py
```

This will test with both Bike Sales and IPL datasets, showing:
- Auto-detected entity columns
- Available metrics
- Sample comparisons
- Available chart types

### Step 3: Launch the Dynamic Dashboard

```bash
streamlit run dynamic_dashboard.py
```

The dashboard will:
1. Open in your browser at `http://localhost:8501`
2. Show all CSV files in a sidebar dropdown
3. Automatically adapt to selected dataset
4. Allow comparison between any two entities

## Usage Examples

### Example 1: Compare IPL Teams

```python
from generic_data_loader import GenericDataLoader
from flexible_analytics_engine import FlexibleAnalyticsEngine

# Load IPL data
loader = GenericDataLoader('ipl_dataset_10000.csv')
analytics = FlexibleAnalyticsEngine(loader)

# Compare teams
comparison = analytics.compare_entities(
    'Chennai Super Kings', 
    'Mumbai Indians'
)

print(analytics.get_comparison_summary(
    'Chennai Super Kings', 
    'Mumbai Indians'
))
```

### Example 2: Generate Visualizations

```python
from dynamic_visualizer import DynamicVisualizer

visualizer = DynamicVisualizer(loader, analytics)

# Create comparison chart
fig = visualizer.plot_metric_comparison(
    'Chennai Super Kings', 
    'Mumbai Indians'
)
fig.show()

# Export to HTML
visualizer.export_chart(fig, 'comparison_chart.html')
```

### Example 3: Time Series Analysis

```python
# Get time series for a metric
ts_data = analytics.get_time_series(
    entity_name='Chennai Super Kings',
    metric_col='runs_scored',
    frequency='W'  # Weekly
)

# Visualize
fig = visualizer.plot_time_series(
    'runs_scored', 
    'Chennai Super Kings', 
    frequency='W'
)
```

### Example 4: Extract Insights

```python
insights = analytics.generate_insights(
    'Chennai Super Kings', 
    'Mumbai Indians'
)

for insight in insights:
    print(f"✓ {insight}")
```

## Dashboard Features

### Tab 1: 📊 Comparison
- Side-by-side entity comparison
- Metrics table with differences
- Categorical distribution analysis

### Tab 2: 📈 Charts
- Metric comparison (grouped bars)
- Category distribution (pie charts)
- Correlation matrices (heatmaps)
- Summary dashboard (multi-panel)

### Tab 3: 🔍 Metrics
- Detailed statistics for selected metric
- Sum, mean, median, min, max, std dev
- Count of records

### Tab 4: 📅 Trends
- Time series visualization
- Adjustable frequency (Daily/Weekly/Monthly)
- Side-by-side entity trends

### Tab 5: 🎯 Insights
- Key findings & comparisons
- Top performers ranking
- Raw data exploration

## Adding New Datasets

### To add your own dataset:

1. **Format Requirements:**
   - CSV file format
   - Must have at least one entity column (team, product, category)
   - Should have numeric metrics for comparison

2. **Place in Project:**
   ```bash
   cp your_dataset.csv /path/to/bike_sales_data/
   ```

3. **Run Dashboard:**
   ```bash
   streamlit run dynamic_dashboard.py
   ```

4. **Select from Dropdown:**
   - Dashboard sidebar will show your dataset
   - Click to analyze

### Example Dataset Structure:

```csv
match_id,team,opponent,venue,runs_scored,wickets_lost,overs_played,result,player_of_match,match_date
1,Chennai Super Kings,Mumbai Indians,Chepauk Stadium,191,9,20,Win,Bumrah,2023-04-01
2,Chennai Super Kings,Mumbai Indians,Chepauk Stadium,189,7,20,Win,MS Dhoni,2023-04-02
...
```

**Required:**
- Entity column (team/product/name) with 2+ unique values
- At least one numeric column for metrics

**Optional:**
- Date column for time series
- Categorical columns for distribution analysis

## API Reference

### GenericDataLoader

```python
loader = GenericDataLoader(csv_path, entity_column=None)

# Properties
loader.entity_column              # Detected entity column name
loader.numeric_columns            # List of numeric metric columns
loader.categorical_columns        # List of categorical columns
loader.date_columns              # List of datetime columns
loader.df                        # Pandas DataFrame

# Methods
loader.get_all_entities()        # List of unique entities
loader.get_entity_data(name)     # DataFrame for specific entity
loader.get_numeric_columns()     # List of metrics
loader.get_categorical_columns() # List of categories
loader.get_summary_stats()       # Dict with overview stats
```

### FlexibleAnalyticsEngine

```python
analytics = FlexibleAnalyticsEngine(loader)

# Methods
analytics.compare_entities(e1, e2)           # Full comparison
analytics.get_entity_aggregates(entity)      # Summary stats
analytics.get_time_series(entity, metric)    # Time series data
analytics.get_top_performers(metric, top_n)  # Ranking
analytics.generate_insights(e1, e2)          # Text insights
analytics.get_comparison_summary(e1, e2)     # Formatted summary
analytics.get_correlation_analysis(entity)   # Correlation matrix
```

### DynamicVisualizer

```python
visualizer = DynamicVisualizer(loader, analytics)

# Methods
visualizer.plot_metric_comparison(e1, e2, metrics)    # Bar chart
visualizer.plot_category_distribution(cat_col, entity) # Pie chart
visualizer.plot_time_series(metric, entity, freq)      # Line chart
visualizer.plot_top_performers(metric, cat_col, top_n) # Ranking chart
visualizer.plot_correlation_heatmap(entity)            # Heatmap
visualizer.create_summary_dashboard(e1, e2)            # Multi-panel
visualizer.export_chart(fig, filename)                 # Save HTML
visualizer.get_available_chart_types()                 # Available charts
```

## Supported CSV Structures

### Structure 1: Product/Model Comparison
```
Product,Date,Sales,Units,Region,Price
Bike A,2023-01-01,10000,5,Delhi,2000
Bike B,2023-01-01,12000,6,Delhi,2000
```

### Structure 2: Sports Team Comparison
```
Team,Date,Runs,Wickets,Venue,Result
Team A,2023-01-01,150,8,Stadium,Win
Team B,2023-01-01,140,9,Stadium,Loss
```

### Structure 3: Company Performance
```
Company,Quarter,Revenue,Employees,Department,Growth
Company A,Q1,1000000,50,Sales,10%
Company B,Q1,1200000,60,Sales,12%
```

### Structure 4: Student Performance
```
Student,Course,Score,Grade,Subject,Semester
Alice,Python,95,A,CS,1
Bob,Python,87,B,CS,1
```

**All work automatically without any code changes!**

## Troubleshooting

### Issue: "No CSV files found"
- **Solution:** Place CSV files in the project directory
- **Check:** Run `ls *.csv` or `dir *.csv`

### Issue: "Entity column not detected"
- **Solution:** CSV must have a column with 2-100 unique values
- **Fix:** Ensure entity column is named with keywords like: team, product, model, category, name

### Issue: "Port 8501 already in use"
- **Solution:** Use different port: `streamlit run dynamic_dashboard.py --server.port 8502`
- **Or:** Kill existing process

### Issue: "No numeric columns found"
- **Solution:** CSV needs at least one numeric column
- **Check:** Column should contain numbers, not text

## Performance Notes

- Tested with 10,000+ records ✓
- Auto-detects structure in <1 second
- Dashboard loads in ~2 seconds
- Comparisons compute in real-time

## Future Enhancements

- [ ] Support for multiple grouping levels
- [ ] Export reports to PDF
- [ ] Predictive analytics
- [ ] Machine learning insights
- [ ] Custom metric definitions
- [ ] Data transformation UI
- [ ] Real-time data streaming

## Files Overview

```
bike_sales_data/
├── generic_data_loader.py          # Universal data loading
├── flexible_analytics_engine.py     # Adaptive analytics
├── dynamic_visualizer.py            # Auto-chart generation
├── dynamic_dashboard.py             # Main Streamlit app
├── test_flexible_system.py          # Test script
├── bike_sales_numeric_sp.csv        # Sample data 1
├── ipl_dataset_10000.csv            # Sample data 2
└── FLEXIBLE_SYSTEM_README.md        # This file
```

## License

This project is provided as-is for educational and commercial use.

---

**🎉 Enjoy your flexible, dataset-agnostic comparison dashboard!**

For questions or issues, check the docstrings in the Python files or run the test script.
