"""
Dynamic Visualization Engine - Works with any dataset.
"""

from typing import Dict, List

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from flexible_analytics_engine import FlexibleAnalyticsEngine
from generic_data_loader import GenericDataLoader


class DynamicVisualizer:
    """Universal visualizer that adapts to any dataset structure."""

    def __init__(self, loader: GenericDataLoader, analytics: FlexibleAnalyticsEngine):
        self.loader = loader
        self.analytics = analytics
        self.colors = [
            "#7dd3fc",
            "#fdba74",
            "#86efac",
            "#c4b5fd",
            "#fde68a",
            "#fca5a5",
            "#99f6e4",
        ]
        self.surface = "rgba(51, 65, 85, 0.94)"
        self.grid = "rgba(226, 232, 240, 0.20)"
        self.font_family = "Space Grotesk, Manrope, sans-serif"

    def _apply_layout(self, fig: go.Figure, title: str, height: int = 520) -> go.Figure:
        fig.update_layout(
            title=dict(text=title, x=0.02, xanchor="left"),
            height=height,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor=self.surface,
            font=dict(family=self.font_family, color="#f8fafc"),
            margin=dict(l=24, r=24, t=72, b=24),
            hoverlabel=dict(bgcolor="#334155", font=dict(color="#f8fafc")),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1.0,
                bgcolor="rgba(51,65,85,0.72)",
            ),
        )
        fig.update_xaxes(showgrid=False, zeroline=False, color="#f8fafc")
        fig.update_yaxes(showgrid=True, gridcolor=self.grid, zeroline=False, color="#f8fafc")
        return fig

    def get_available_chart_types(self) -> Dict[str, List[str]]:
        available_charts = {}
        if len(self.loader.numeric_columns) >= 1:
            available_charts["Single Metric"] = ["bar", "line", "box"]
        if len(self.loader.numeric_columns) >= 2:
            available_charts["Metric Comparison"] = ["grouped_bar", "scatter", "correlation"]
        if len(self.loader.categorical_columns) >= 1:
            available_charts["Category Analysis"] = ["pie", "horizontal_bar", "sunburst"]
        if self.loader.date_columns and len(self.loader.numeric_columns) >= 1:
            available_charts["Time Series"] = ["line_trend", "area", "bar_trend"]
        return available_charts

    def plot_metric_comparison(
        self,
        entity1: str,
        entity2: str,
        metric_cols: List[str] = None,
        normalize: bool = False,
        orientation: str = "v",
    ) -> go.Figure:
        if not metric_cols:
            metric_cols = self.loader.numeric_columns[:5]

        data1 = self.loader.get_entity_data(entity1)
        data2 = self.loader.get_entity_data(entity2)
        metrics_data = {"Metric": [], entity1: [], entity2: []}

        for col in metric_cols:
            if col not in data1.columns or col not in data2.columns:
                continue
            val1 = pd.to_numeric(data1[col], errors="coerce").sum()
            val2 = pd.to_numeric(data2[col], errors="coerce").sum()
            if pd.notna(val1) and pd.notna(val2):
                metrics_data["Metric"].append(col)
                metrics_data[entity1].append(val1)
                metrics_data[entity2].append(val2)

        if not metrics_data["Metric"]:
            return go.Figure().add_annotation(text="No metrics available for comparison")

        df_plot = pd.DataFrame(metrics_data)
        if normalize:
            max_vals = df_plot[[entity1, entity2]].max(axis=1).replace(0, 1)
            df_plot[entity1] = df_plot[entity1] / max_vals
            df_plot[entity2] = df_plot[entity2] / max_vals

        is_horizontal = orientation == "h"
        fig = go.Figure(
            data=[
                go.Bar(
                    name=entity1,
                    x=df_plot[entity1] if is_horizontal else df_plot["Metric"],
                    y=df_plot["Metric"] if is_horizontal else df_plot[entity1],
                    orientation=orientation,
                    marker=dict(color=self.colors[0], line=dict(color="#f8fafc", width=1)),
                    text=df_plot[entity1],
                    textposition="auto",
                ),
                go.Bar(
                    name=entity2,
                    x=df_plot[entity2] if is_horizontal else df_plot["Metric"],
                    y=df_plot["Metric"] if is_horizontal else df_plot[entity2],
                    orientation=orientation,
                    marker=dict(color=self.colors[1], line=dict(color="#f8fafc", width=1)),
                    text=df_plot[entity2],
                    textposition="auto",
                ),
            ]
        )
        fig.update_layout(barmode="group", hovermode="x unified")
        if is_horizontal:
            fig.update_xaxes(title="Normalized Value" if normalize else "Value", showgrid=True, gridcolor=self.grid)
        else:
            fig.update_yaxes(title="Normalized Value" if normalize else "Value")
        return self._apply_layout(fig, f"{entity1} vs {entity2} | KPI Comparison", height=540)

    def plot_category_distribution(
        self, category_col: str = None, entity_name: str = None, top_n: int = 8
    ) -> go.Figure:
        if not category_col:
            category_col = self.loader.categorical_columns[0] if self.loader.categorical_columns else None
        if not category_col:
            return None

        data = self.loader.get_entity_data(entity_name) if entity_name else self.loader.df
        distribution = data[category_col].value_counts().head(top_n)
        fig = go.Figure(
            data=[
                go.Pie(
                    labels=distribution.index.astype(str),
                    values=distribution.values,
                    hole=0.52,
                    marker=dict(colors=self.colors[: len(distribution)]),
                    textinfo="label+percent",
                )
            ]
        )

        title = f"{category_col} Distribution"
        if entity_name:
            title += f" | {entity_name}"
        fig.update_traces(sort=False)
        return self._apply_layout(fig, title, height=500)

    def plot_time_series(
        self,
        metric_col: str = None,
        entity_name: str = None,
        frequency: str = "D",
        date_col: str = None,
    ) -> go.Figure:
        if not metric_col:
            metric_col = self.loader.numeric_columns[0] if self.loader.numeric_columns else None
        if not metric_col or not self.loader.date_columns:
            return None

        ts_data = self.analytics.get_time_series(
            entity_name=entity_name,
            metric_col=metric_col,
            date_col=date_col,
            frequency=frequency,
        )
        if ts_data.empty:
            return None

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=ts_data.index,
                y=ts_data["sum"],
                mode="lines+markers",
                name="Total",
                line=dict(color=self.colors[0], width=3),
                marker=dict(size=7, color="#0f172a", line=dict(color=self.colors[0], width=2)),
                fill="tozeroy",
                fillcolor="rgba(56,189,248,0.16)",
            )
        )

        title = f"{metric_col} Over Time"
        if entity_name:
            title += f" | {entity_name}"
        fig.update_yaxes(title=metric_col)
        return self._apply_layout(fig, title, height=500)

    def plot_top_performers(
        self, metric_col: str = None, categorical_col: str = None, top_n: int = 10
    ) -> go.Figure:
        if not metric_col:
            metric_col = self.loader.numeric_columns[0] if self.loader.numeric_columns else None
        if not categorical_col:
            categorical_col = self.loader.categorical_columns[0] if self.loader.categorical_columns else None
        if not metric_col or not categorical_col:
            return None

        top_data = self.analytics.get_top_performers(metric_col, top_n, categorical_col)
        if not top_data or not top_data.get("data"):
            return None

        data_dict = top_data["data"]
        fig = go.Figure(
            data=[
                go.Bar(
                    x=list(data_dict.values()),
                    y=list(data_dict.keys()),
                    orientation="h",
                    marker=dict(
                        color=list(data_dict.values()),
                        colorscale=[[0, self.colors[0]], [1, self.colors[1]]],
                        line=dict(color="#f8fafc", width=1),
                    ),
                    text=list(data_dict.values()),
                    textposition="auto",
                )
            ]
        )
        fig.update_yaxes(autorange="reversed", title=categorical_col)
        fig.update_xaxes(title=metric_col, showgrid=True, gridcolor=self.grid)
        return self._apply_layout(fig, f"Top {top_n} {categorical_col} by {metric_col}", height=540)

    def plot_correlation_heatmap(self, entity_name: str = None) -> go.Figure:
        if len(self.loader.numeric_columns) < 2:
            return None

        corr_matrix = self.analytics.get_correlation_analysis(entity_name)
        fig = go.Figure(
            data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale=[[0.0, "#1d4ed8"], [0.5, "#0f172a"], [1.0, "#f97316"]],
                zmid=0,
                text=corr_matrix.values,
                texttemplate="%{text:.2f}",
                textfont={"size": 10},
                hoverongaps=False,
            )
        )

        title = "Correlation Matrix"
        if entity_name:
            title += f" | {entity_name}"
        fig.update_xaxes(side="bottom")
        return self._apply_layout(fig, title, height=620)

    def create_summary_dashboard(self, entity1: str, entity2: str) -> go.Figure:
        metrics = self.loader.numeric_columns[:4]
        fig = make_subplots(
            rows=2,
            cols=2,
            subplot_titles=[metric[:22] for metric in metrics],
            specs=[[{"type": "bar"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]],
            horizontal_spacing=0.14,
            vertical_spacing=0.16,
        )

        row_col_pairs = [(1, 1), (1, 2), (2, 1), (2, 2)]
        for metric, (row, col) in zip(metrics, row_col_pairs):
            try:
                data1 = pd.to_numeric(self.loader.get_entity_data(entity1)[metric], errors="coerce").sum()
                data2 = pd.to_numeric(self.loader.get_entity_data(entity2)[metric], errors="coerce").sum()
                fig.add_trace(
                    go.Bar(name=entity1, x=[entity1], y=[data1], marker_color=self.colors[0], showlegend=row == 1 and col == 1),
                    row=row,
                    col=col,
                )
                fig.add_trace(
                    go.Bar(name=entity2, x=[entity2], y=[data2], marker_color=self.colors[1], showlegend=row == 1 and col == 1),
                    row=row,
                    col=col,
                )
            except Exception:
                continue

        fig.update_layout(barmode="group", hovermode="x unified")
        return self._apply_layout(fig, f"Summary Dashboard | {entity1} vs {entity2}", height=900)

    def export_chart(self, fig: go.Figure, filename: str):
        fig.write_html(filename)
        print(f"Chart exported: {filename}")
