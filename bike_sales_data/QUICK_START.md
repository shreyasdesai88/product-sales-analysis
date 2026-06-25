# 🚀 QUICK START REFERENCE CARD

## Installation (1 Step)
```bash
pip install -r requirements.txt
```

## Run Dashboard (1 Command)
```bash
streamlit run dynamic_dashboard.py
```
Opens: `http://localhost:8501`

---

## Dashboard Usage

### Step 1: Select Dataset
- Dropdown in sidebar shows all CSV files
- Select your dataset
- Dashboard auto-adapts

### Step 2: Choose Entities
- Select 2 entities to compare (teams, products, etc.)
- Auto-detected from CSV

### Step 3: Explore Tabs
| Tab | Features |
|-----|----------|
| 📊 **Comparison** | Side-by-side metrics, categorical data |
| 📈 **Charts** | Bar charts, pie charts, heatmaps, summary |
| 🔍 **Metrics** | Detailed statistics (sum, mean, median, etc.) |
| 📅 **Trends** | Time series analysis by day/week/month |
| 🎯 **Insights** | Findings, top performers, raw data |

---

## Python API Usage

### Load Any Dataset
```python
from generic_data_loader import GenericDataLoader

loader = GenericDataLoader('your_file.csv')
entities = loader.get_all_entities()  # ['Team1', 'Team2', ...]
```

### Compare Entities
```python
from flexible_analytics_engine import FlexibleAnalyticsEngine

analytics = FlexibleAnalyticsEngine(loader)
comparison = analytics.compare_entities('Entity1', 'Entity2')
```

### Create Visualizations
```python
from dynamic_visualizer import DynamicVisualizer

visualizer = DynamicVisualizer(loader, analytics)
fig = visualizer.plot_metric_comparison('Entity1', 'Entity2')
fig.show()  # Interactive chart
```

---

## Dataset Requirements

**Minimal CSV Format:**
```
entity_column, metric1, metric2, category1, date
Value1, 100, 50, CatA, 2023-01-01
Value2, 120, 45, CatB, 2023-01-02
```

**Requirements:**
- At least 1 column with 2+ unique values (entity)
- At least 1 numeric column (metric)
- Optional: date column for trends
- Optional: categorical columns for distribution

---

## CLI Commands

### Run Tests
```bash
python test_flexible_system.py
```
Tests both Bike Sales and IPL data

### Run IPL Demo
```bash
python demo_ipl_comparison.py
```
Shows IPL teams comparison with all metrics

### Launch Dashboard
```bash
streamlit run dynamic_dashboard.py
```

### Use Different Port
```bash
streamlit run dynamic_dashboard.py --server.port 8502
```

---

## API Quick Reference

### GenericDataLoader
```python
loader = GenericDataLoader('data.csv')

# Properties
loader.entity_column           # Detected entity column
loader.numeric_columns         # List of metrics
loader.categorical_columns     # List of attributes
loader.date_columns           # List of dates
loader.df                     # Raw DataFrame

# Methods
loader.get_all_entities()              # All unique entities
loader.get_entity_data('Entity1')       # DataFrame for entity
loader.get_numeric_columns()            # Available metrics
loader.get_summary_stats()              # Dataset overview
```

### FlexibleAnalyticsEngine
```python
analytics = FlexibleAnalyticsEngine(loader)

# Main methods
analytics.compare_entities('E1', 'E2')      # Full comparison
analytics.generate_insights('E1', 'E2')     # Text insights
analytics.get_time_series('E1')             # Time series data
analytics.get_entity_aggregates('E1')       # Summary stats
analytics.get_top_performers()              # Ranking
analytics.get_correlation_analysis('E1')    # Correlations
```

### DynamicVisualizer
```python
visualizer = DynamicVisualizer(loader, analytics)

# Chart methods
visualizer.plot_metric_comparison(e1, e2)       # Bar chart
visualizer.plot_category_distribution(col)      # Pie chart
visualizer.plot_time_series(metric, entity)     # Line chart
visualizer.plot_correlation_heatmap(entity)     # Heatmap
visualizer.plot_top_performers(metric, cat)     # Ranking
visualizer.create_summary_dashboard(e1, e2)     # Multi-panel
visualizer.export_chart(fig, 'file.html')       # Save
```

---

## Common Tasks

### Compare Two Teams
```python
from generic_data_loader import GenericDataLoader
from flexible_analytics_engine import FlexibleAnalyticsEngine

loader = GenericDataLoader('ipl_dataset_10000.csv')
analytics = FlexibleAnalyticsEngine(loader)

print(analytics.get_comparison_summary('Chennai Super Kings', 'Mumbai Indians'))
```

### Get Top 10 Performers
```python
top = analytics.get_top_performers(
    metric_col='runs_scored',
    top_n=10
)
for name, value in top['data'].items():
    print(f"{name}: {value:,.0f}")
```

### Export Chart to HTML
```python
from dynamic_visualizer import DynamicVisualizer

visualizer = DynamicVisualizer(loader, analytics)
fig = visualizer.plot_metric_comparison('E1', 'E2')
visualizer.export_chart(fig, 'comparison.html')
```

### Time Series Analysis
```python
ts = analytics.get_time_series(
    entity_name='Chennai Super Kings',
    metric_col='runs_scored',
    frequency='W'  # W=Weekly, M=Monthly, D=Daily
)
print(ts.head())
```

---

## File Structure

```
bike_sales_data/
├── generic_data_loader.py              ← Auto-detect structure
├── flexible_analytics_engine.py         ← Compare entities
├── dynamic_visualizer.py                ← Create charts
├── dynamic_dashboard.py                 ← Interactive app
│
├── test_flexible_system.py              ← Run tests
├── demo_ipl_comparison.py               ← See IPL example
│
├── bike_sales_numeric_sp.csv            ← Sample 1
├── ipl_dataset_10000.csv                ← Sample 2
│
├── FLEXIBLE_SYSTEM_README.md            ← Full docs
└── IMPLEMENTATION_SUMMARY.md            ← Implementation
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8501 in use | Use different port: `--server.port 8502` |
| No CSV files found | Place CSV files in project directory |
| Entity not detected | CSV must have column with 2-100 unique values |
| No metrics | CSV needs numeric columns |
| Charts not showing | Check data has required columns |

---

## Examples by Use Case

### 📊 Product Comparison
```python
loader = GenericDataLoader('products.csv')  # Entity: product_name
analytics = FlexibleAnalyticsEngine(loader)
analytics.compare_entities('Product A', 'Product B')
```

### 🏏 Sports Teams
```python
loader = GenericDataLoader('cricket.csv')  # Entity: team
analytics = FlexibleAnalyticsEngine(loader)
analytics.compare_entities('CSK', 'MI')
```

### 🏢 Company Performance
```python
loader = GenericDataLoader('companies.csv')  # Entity: company
analytics = FlexibleAnalyticsEngine(loader)
analytics.compare_entities('Apple', 'Microsoft')
```

### 🎓 Student Performance
```python
loader = GenericDataLoader('students.csv')  # Entity: student_name
analytics = FlexibleAnalyticsEngine(loader)
analytics.compare_entities('Student1', 'Student2')
```

---

## Tips & Tricks

1. **Column Naming:** Use keywords like `team`, `product`, `model`, `category` for auto-detection
2. **Date Format:** Use ISO format (2023-01-01) for date columns
3. **Numeric Data:** Numbers can be int or float - system converts automatically
4. **Large Datasets:** Works fine with 100K+ records
5. **Multiple Metrics:** System auto-selects top 5 for display
6. **Export Reports:** Dashboard has export option for each chart

---

## Support

- **Full Docs:** See `FLEXIBLE_SYSTEM_README.md`
- **Examples:** Run `python demo_ipl_comparison.py`
- **Tests:** Run `python test_flexible_system.py`
- **Code Help:** Check docstrings in Python files

---

## 🎉 You're Ready!

```bash
streamlit run dynamic_dashboard.py
```

Select your dataset → Compare entities → Explore insights! 🚀

No configuration. No code changes. Just works! ✨
