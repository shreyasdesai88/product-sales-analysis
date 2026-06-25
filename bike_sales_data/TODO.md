# TODO - AI ML Sales Optimization Enhancement

## Step 1: Add ML module
- Create `ml_sales_optimizer.py` implementing:
  - time-series forecasting for selected KPI using detected date column
  - pricing optimization: learn KPI ~ Price (+ optional date trend) and search best price within observed bounds

## Step 2: Update dashboard UI
- Update `dynamic_dashboard.py` to add a new tab/section (e.g., “AI Optimization”):
  - KPI selector (use `st.session_state.selected_kpis`)
  - choose forecast horizon/frequency (use date column)
  - show forecast plot + best price recommendation

## Step 3: Add dependencies
- Update `requirements.txt` to include any needed packages.
  - (scikit-learn is likely available, but must be declared)

## Step 4: Tests
- Add `test_ml_sales_optimizer.py` with lightweight functional tests using `bike_sales_numeric_sp.csv`.

## Step 5: Quick verification
- Run existing tests + new tests.
- (Optional) run dashboard locally if streamlit works.

