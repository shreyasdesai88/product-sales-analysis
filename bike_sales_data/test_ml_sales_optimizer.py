import pandas as pd

from generic_data_loader import GenericDataLoader
from flexible_analytics_engine import FlexibleAnalyticsEngine
from ml_sales_optimizer import MLSalesOptimizer


def test_forecast_and_optimize_bike_sales():
    loader = GenericDataLoader("bike_sales_numeric_sp.csv")
    analytics = FlexibleAnalyticsEngine(loader)
    optimizer = MLSalesOptimizer(loader, analytics)

    entities = loader.get_all_entities()
    assert len(entities) >= 2

    entity = entities[0]
    # Prefer common target KPI names
    target_kpi = "Total_Sales" if "Total_Sales" in loader.df.columns else (loader.numeric_columns[0] if loader.numeric_columns else None)
    assert target_kpi is not None

    assert loader.date_columns, "Dataset must have a date column for forecasting"

    forecast = optimizer.forecast_target(
        entity_name=entity,
        target_kpi=target_kpi,
        frequency="W",
        horizon_steps=3,
    )

    assert not forecast.forecast.empty
    assert "prediction" in forecast.forecast.columns

    if optimizer.price_col is not None:
        opt = optimizer.optimize_price(
            entity_name=entity,
            target_kpi=target_kpi,
            min_price=None,
            max_price=None,
            grid_size=25,
        )
        assert opt.best_price >= opt.bounds[0]
        assert opt.best_price <= opt.bounds[1]
        assert opt.best_predicted_target is not None


if __name__ == "__main__":
    test_forecast_and_optimize_bike_sales()
    print("ML optimizer tests passed")

