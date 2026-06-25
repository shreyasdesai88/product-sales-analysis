"""ML Sales Optimizer

Adds lightweight ML capabilities to the Flexible Comparison Dashboard.

Features:
- Demand forecasting for a chosen KPI (user-selected metric)
- Price optimization: train relationship KPI ~ Price (+ date trend) and recommend a best price

Notes:
- This module is dataset-agnostic but relies on the dataset having:
  - a date column (detected by GenericDataLoader)
  - a price column named "Price" (case-insensitive)
  - a target KPI chosen by the dashboard
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd

# Optional dependency: scikit-learn
# The Streamlit UI should not crash if sklearn is missing.
try:
    from sklearn.linear_model import LinearRegression  # type: ignore
except ModuleNotFoundError:  # pragma: no cover
    LinearRegression = None



def _find_case_insensitive_column(columns: List[str], wanted: str) -> Optional[str]:
    wanted_l = wanted.lower()
    for c in columns:
        if c.lower() == wanted_l:
            return c
    return None


def _ensure_datetime(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    out = df.copy()
    out[date_col] = pd.to_datetime(out[date_col], errors="coerce")
    out = out.dropna(subset=[date_col])
    return out


def _prepare_time_feature(df: pd.DataFrame, date_col: str) -> Tuple[pd.Series, float]:
    # Convert to numeric time (days since start)
    t0 = df[date_col].min()
    t_days = (df[date_col] - t0).dt.total_seconds() / (24 * 3600)
    return t_days, float(t0.value)


@dataclass
class ForecastResult:
    target: str
    date_col: str
    horizon_steps: int
    frequency: str
    forecast: pd.DataFrame  # columns: [date_col, prediction]


@dataclass
class PriceOptimizationResult:
    target: str
    price_col: str
    best_price: float
    best_predicted_target: float
    baseline_price: float
    baseline_predicted_target: float
    bounds: Tuple[float, float]


class MLSalesOptimizer:
    """Train/predict and compute price recommendation."""

    def __init__(self, loader, analytics=None):
        self.loader = loader
        self.analytics = analytics
        self.df = loader.df
        self.entity_column = loader.entity_column

        self.date_columns = getattr(loader, "date_columns", [])
        self.numeric_columns = getattr(loader, "numeric_columns", [])

        self.price_col = _find_case_insensitive_column(list(self.df.columns), "price")

    def _get_date_col(self, date_col: Optional[str] = None) -> Optional[str]:
        if date_col:
            if date_col in self.df.columns:
                return date_col
            # allow case-insensitive
            for c in self.df.columns:
                if c.lower() == date_col.lower():
                    return c
        return self.date_columns[0] if self.date_columns else None

    def _filter_entity(self, entity_name: str) -> pd.DataFrame:
        if not self.entity_column:
            return self.df.copy()
        return self.df[self.df[self.entity_column] == entity_name].copy()

    def forecast_target(
        self,
        entity_name: str,
        target_kpi: str,
        date_col: Optional[str] = None,
        frequency: str = "W",
        horizon_steps: int = 8,
    ) -> ForecastResult:
        """Forecast KPI using linear regression on time.

        Aggregates by date frequency and predicts future trend.
        """
        df = self._filter_entity(entity_name)
        date_col = self._get_date_col(date_col)
        if not date_col:
            raise ValueError("No date column available for forecasting")
        if target_kpi not in df.columns:
            raise ValueError(f"Target KPI '{target_kpi}' not found")

        df = _ensure_datetime(df, date_col)

        # aggregate by frequency
        df[target_kpi] = pd.to_numeric(df[target_kpi], errors="coerce")
        df = df.dropna(subset=[target_kpi])
        if df.empty:
            raise ValueError("No numeric data available for forecasting")

        agg = (
            df.groupby(pd.Grouper(key=date_col, freq=frequency))[target_kpi]
            .mean()
            .dropna()
            .reset_index()
        )
        if len(agg) < 2:
            raise ValueError("Not enough data points to train a forecast")

        t, _ = _prepare_time_feature(agg, date_col)
        X = t.values.reshape(-1, 1)
        y = agg[target_kpi].values

        if LinearRegression is None:
            raise ModuleNotFoundError(
                "scikit-learn is required for forecasting/optimization. Install it with: pip install -r requirements.txt"
            )

        model = LinearRegression()
        model.fit(X, y)




        t_last = float(t.max())
        # future points in frequency steps
        future_dates = pd.date_range(start=agg[date_col].max(), periods=horizon_steps + 1, freq=frequency)[
            1:
        ]
        t_future = (future_dates - agg[date_col].min()).total_seconds() / (24 * 3600)
        pred = model.predict(t_future.values.reshape(-1, 1))

        forecast_df = pd.DataFrame({date_col: future_dates, "prediction": pred})
        return ForecastResult(
            target=target_kpi,
            date_col=date_col,
            horizon_steps=horizon_steps,
            frequency=frequency,
            forecast=forecast_df,
        )

    def optimize_price(
        self,
        entity_name: str,
        target_kpi: str,
        date_col: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        grid_size: int = 40,
    ) -> PriceOptimizationResult:
        """Recommend a best price by learning KPI ~ Price + date trend (linear model).

        Searches price within observed bounds (or user-provided min/max).
        """
        df = self._filter_entity(entity_name)
        date_col = self._get_date_col(date_col)
        if not date_col:
            raise ValueError("No date column available for price optimization")
        if self.price_col is None:
            raise ValueError("No Price column found in dataset")
        if target_kpi not in df.columns:
            raise ValueError(f"Target KPI '{target_kpi}' not found")

        df = _ensure_datetime(df, date_col)
        df[self.price_col] = pd.to_numeric(df[self.price_col], errors="coerce")
        df[target_kpi] = pd.to_numeric(df[target_kpi], errors="coerce")
        df = df.dropna(subset=[self.price_col, target_kpi])
        if df.empty:
            raise ValueError("No numeric data available for price optimization")

        # Bounds
        p_min_obs = float(df[self.price_col].min())
        p_max_obs = float(df[self.price_col].max())
        lo = p_min_obs if min_price is None else float(min_price)
        hi = p_max_obs if max_price is None else float(max_price)
        if lo >= hi:
            raise ValueError("Invalid price bounds for optimization")

        # Baseline price = median observed
        baseline_price = float(df[self.price_col].median())

        # Prepare time feature to help generalize.
        t_days, _ = _prepare_time_feature(df, date_col)
        X = np.column_stack([
            df[self.price_col].values,
            t_days.values,
        ])
        y = df[target_kpi].values

        model = LinearRegression()
        model.fit(X, y)

        # Choose a time anchor for price recommendation: most recent date.
        t_anchor = float(t_days.max())
        grid = np.linspace(lo, hi, grid_size)
        X_grid = np.column_stack([grid, np.full_like(grid, t_anchor)])
        y_grid = model.predict(X_grid)

        idx = int(np.nanargmax(y_grid))
        best_price = float(grid[idx])
        best_pred = float(y_grid[idx])

        baseline_pred = float(
            model.predict(np.array([[baseline_price, t_anchor]]))[0]
        )

        return PriceOptimizationResult(
            target=target_kpi,
            price_col=self.price_col,
            best_price=best_price,
            best_predicted_target=best_pred,
            baseline_price=baseline_price,
            baseline_predicted_target=baseline_pred,
            bounds=(lo, hi),
        )

