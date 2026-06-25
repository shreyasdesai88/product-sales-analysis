"""
Dynamic Dashboard - Automatically adapts to any dataset structure.
"""

import hashlib
import os
import tempfile
from pathlib import Path

import pandas as pd
import streamlit as st

from flexible_analytics_engine import FlexibleAnalyticsEngine
from generic_data_loader import GenericDataLoader
from dynamic_visualizer import DynamicVisualizer


st.set_page_config(
    page_title="Flexible Comparison Dashboard",
    page_icon="analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

SCRIPT_DIR = Path(__file__).parent
os.chdir(SCRIPT_DIR)

ACCENT = "#67e8f9"
ACCENT_ALT = "#fb923c"
SURFACE = "#1e293b"
TEXT_MUTED = "#cbd5e1"


def inject_theme() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Manrope:wght@400;500;600;700&display=swap');

        :root {{
            --bg: #020617;
            --surface: {SURFACE};
            --surface-strong: #334155;
            --ink: #f8fafc;
            --muted: {TEXT_MUTED};
            --line: rgba(226, 232, 240, 0.22);
            --accent: {ACCENT};
            --accent-2: {ACCENT_ALT};
            --shadow: 0 22px 56px rgba(2, 6, 23, 0.45);
            --radius: 22px;
        }}

        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(56, 189, 248, 0.18), transparent 24%),
                radial-gradient(circle at top right, rgba(249, 115, 22, 0.18), transparent 28%),
                radial-gradient(circle at bottom center, rgba(139, 92, 246, 0.12), transparent 22%),
                linear-gradient(180deg, #020617 0%, #0f172a 46%, #111827 100%);
            color: var(--ink);
            font-family: "Manrope", sans-serif;
        }}

        h1, h2, h3, .stMarkdown strong {{
            font-family: "Space Grotesk", sans-serif;
            color: var(--ink);
            letter-spacing: -0.02em;
        }}

        p, li, label, .stCaption, .stMarkdown, .stText {{
            color: var(--ink);
        }}

        small, .panel-copy, .hero-copy, .stat-sub, .section-label {{
            color: var(--muted);
        }}

        [data-testid="stSidebar"] {{
            background:
                linear-gradient(180deg, rgba(15,23,42,0.98) 0%, rgba(30,41,59,0.98) 100%);
            border-right: 1px solid var(--line);
        }}

        [data-testid="stSidebar"] * {{
            color: #f8fafc !important;
        }}

        [data-testid="stSidebar"] .block-container {{
            padding-top: 1.4rem;
        }}

        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 2rem;
            max-width: 1280px;
        }}

        div[data-testid="stMetric"] {{
            background: rgba(30,41,59,0.94);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 0.85rem 1rem;
            box-shadow: 0 10px 24px rgba(2, 6, 23, 0.20);
        }}

        .hero-card {{
            background:
                linear-gradient(135deg, rgba(30,41,59,0.98), rgba(51,65,85,0.94)),
                linear-gradient(120deg, rgba(103,232,249,0.14), rgba(251,146,60,0.10));
            border: 1px solid rgba(226, 232, 240, 0.24);
            border-radius: 28px;
            box-shadow: var(--shadow);
            padding: 1.6rem 1.6rem 1.2rem 1.6rem;
            margin-bottom: 1rem;
        }}

        .hero-kicker {{
            display: inline-block;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: rgba(56,189,248,0.14);
            color: var(--accent);
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}

        .hero-title {{
            margin: 0.85rem 0 0.5rem 0;
            font-size: 2.3rem;
            line-height: 1;
        }}

        .hero-copy {{
            color: var(--muted);
            font-size: 1rem;
            margin-bottom: 0.9rem;
        }}

        .badge-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 0.55rem;
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.42rem 0.8rem;
            border-radius: 999px;
            background: rgba(255,255,255,0.12);
            color: var(--ink);
            font-size: 0.84rem;
            font-weight: 600;
        }}

        .panel {{
            background: rgba(30, 41, 59, 0.90);
            border: 1px solid var(--line);
            border-radius: 24px;
            box-shadow: 0 14px 36px rgba(2, 6, 23, 0.18);
            padding: 1.1rem 1.1rem 0.9rem 1.1rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(8px);
        }}

        .panel h3 {{
            margin-top: 0;
            margin-bottom: 0.3rem;
        }}

        .panel-copy {{
            color: var(--muted);
            margin-bottom: 0.85rem;
            font-size: 0.94rem;
        }}

        .stat-card {{
            background: linear-gradient(180deg, rgba(51,65,85,0.96), rgba(71,85,105,0.90));
            border: 1px solid var(--line);
            border-radius: 20px;
            box-shadow: 0 12px 26px rgba(2, 6, 23, 0.22);
            padding: 1rem;
            min-height: 132px;
        }}

        .stat-label {{
            color: var(--muted);
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
        }}

        .stat-value {{
            margin-top: 0.45rem;
            font-size: 1.75rem;
            line-height: 1.05;
            font-weight: 700;
            font-family: "Space Grotesk", sans-serif;
        }}

        .stat-sub {{
            margin-top: 0.45rem;
            color: var(--muted);
            font-size: 0.9rem;
        }}

        .insight-card {{
            background: linear-gradient(135deg, rgba(103,232,249,0.18), rgba(51,65,85,0.94));
            border: 1px solid rgba(103,232,249,0.28);
            border-radius: 18px;
            padding: 0.95rem 1rem;
            margin-bottom: 0.75rem;
            color: var(--ink);
        }}

        .insight-empty {{
            background: rgba(51,65,85,0.88);
            border: 1px dashed rgba(226, 232, 240, 0.26);
            border-radius: 18px;
            padding: 1rem;
            color: var(--muted);
        }}

        .section-label {{
            color: var(--muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-size: 0.76rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }}

        .dataframe-container {{
            border-radius: 18px;
            overflow: hidden;
        }}

        div[data-baseweb="tab-list"] {{
            gap: 0.45rem;
            background: rgba(51, 65, 85, 0.88);
            padding: 0.35rem;
            border-radius: 999px;
            border: 1px solid rgba(226, 232, 240, 0.22);
        }}

        button[data-baseweb="tab"] {{
            background: rgba(255,255,255,0.18);
            border-radius: 999px;
            border: 1px solid rgba(226, 232, 240, 0.26);
            padding: 0.52rem 1.05rem;
            color: #f8fafc;
            font-weight: 700;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
        }}

        button[data-baseweb="tab"][aria-selected="true"] {{
            background: linear-gradient(135deg, rgba(56,189,248,0.95), rgba(249,115,22,0.92));
            border-color: rgba(255,255,255,0.42);
            color: #ffffff;
            box-shadow: 0 0 0 3px rgba(56,189,248,0.18), 0 10px 24px rgba(56,189,248,0.22);
        }}

        button[data-baseweb="tab"]:hover {{
            background: rgba(56,189,248,0.22);
            border-color: rgba(56,189,248,0.38);
            color: #ffffff;
        }}

        .stSelectbox label, .stMultiSelect label, .stRadio label, .stSlider label {{
            font-weight: 600;
            color: #f8fafc !important;
        }}

        [data-baseweb="select"] > div,
        .stMultiSelect [data-baseweb="select"] > div,
        .stTextInput > div > div > input,
        .stNumberInput input,
        .stDateInput input,
        .stTextArea textarea {{
            background: rgba(51,65,85,0.92) !important;
            color: #f8fafc !important;
            border: 1px solid rgba(226,232,240,0.24) !important;
        }}

        .stRadio [role="radiogroup"],
        .stSlider,
        .stExpander {{
            background: rgba(51,65,85,0.50);
            border-radius: 16px;
            padding: 0.35rem;
        }}

        div[data-testid="stFileUploader"] {{
            background: linear-gradient(135deg, rgba(8,47,73,0.98), rgba(14,116,144,0.92));
            border: 1px solid rgba(103,232,249,0.42);
            border-radius: 20px;
            padding: 0.75rem;
            box-shadow: 0 14px 32px rgba(6, 182, 212, 0.18);
        }}

        div[data-testid="stFileUploader"] * {{
            color: #f0f9ff !important;
        }}

        div[data-testid="stFileUploader"] section {{
            background: linear-gradient(135deg, rgba(12,74,110,0.96), rgba(14,116,144,0.88)) !important;
            border: 2px dashed rgba(125,211,252,0.75) !important;
            border-radius: 18px !important;
        }}

        div[data-testid="stFileUploader"] section:hover {{
            background: linear-gradient(135deg, rgba(14,116,144,0.98), rgba(6,182,212,0.92)) !important;
            border-color: rgba(165,243,252,0.95) !important;
        }}

        div[data-testid="stFileUploader"] button {{
            background: linear-gradient(135deg, rgba(103,232,249,0.92), rgba(59,130,246,0.92)) !important;
            color: #082f49 !important;
            border: 0 !important;
            font-weight: 800 !important;
            border-radius: 12px !important;
        }}

        [data-testid="stDataFrame"] {{
            background: rgba(51,65,85,0.92);
            border: 1px solid rgba(226,232,240,0.22);
            border-radius: 18px;
        }}

        [data-testid="stDataFrame"] * {{
            color: #f8fafc !important;
        }}

        div[data-testid="stAlert"] {{
            background: rgba(51,65,85,0.92);
            color: #f8fafc;
            border: 1px solid rgba(226,232,240,0.22);
        }}

        code {{
            color: #e0f2fe;
            background: rgba(255,255,255,0.10);
            padding: 0.15rem 0.35rem;
            border-radius: 8px;
        }}

        .stButton > button {{
            width: 100%;
            border-radius: 14px;
            border: 1px solid rgba(56,189,248,0.22);
            background: linear-gradient(135deg, rgba(56,189,248,0.16), rgba(249,115,22,0.10));
            color: #e2e8f0;
            font-weight: 700;
            padding: 0.55rem 0.8rem;
        }}

        .stButton > button:hover {{
            border-color: rgba(56,189,248,0.42);
            background: linear-gradient(135deg, rgba(56,189,248,0.24), rgba(249,115,22,0.16));
            color: #ffffff;
        }}

        .footer-note {{
            color: var(--muted);
            text-align: center;
            padding: 0.4rem 0 0.8rem 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_value(value) -> str:
    if value is None or pd.isna(value):
        return "-"
    abs_value = abs(float(value))
    if abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if abs_value >= 1_000:
        return f"{value / 1_000:.1f}K"
    if abs_value >= 100:
        return f"{value:,.0f}"
    return f"{value:,.2f}"


def render_section(title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="panel">
            <div class="section-label">Dashboard Section</div>
            <h3>{title}</h3>
            <div class="panel-copy">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_stat_card(label: str, value: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_metric_table(comparison: dict, entity1: str, entity2: str, selected_kpis: list[str]) -> pd.DataFrame:
    rows = []
    for metric, values in comparison.get("metrics", {}).items():
        if metric not in selected_kpis:
            continue
        e1_sum = values[entity1]["sum"]
        e2_sum = values[entity2]["sum"]
        diff = e1_sum - e2_sum
        winner = entity1 if diff > 0 else entity2 if diff < 0 else "Tie"
        rows.append(
            {
                "Metric": metric,
                entity1: e1_sum,
                entity2: e2_sum,
                "Difference": diff,
                "Leader": winner,
            }
        )
    return pd.DataFrame(rows)


def style_metric_table(df: pd.DataFrame):
    styled = df.copy()
    for col in styled.columns:
        if col not in {"Metric", "Leader"}:
            styled[col] = styled[col].map(format_value)

    return styled.style.hide(axis="index").set_properties(
        subset=["Metric", "Leader"], **{"font-weight": "600"}
    )


def render_insight(text: str) -> None:
    st.markdown(f'<div class="insight-card">{text}</div>', unsafe_allow_html=True)


inject_theme()

st.sidebar.markdown(
    """
    <div style="padding:0.3rem 0 0.8rem 0;">
        <div class="section-label">Control Room</div>
        <h2 style="margin:0;">Dataset Studio</h2>
        <div class="panel-copy" style="margin:0.25rem 0 0 0;">
            Choose a dataset, tune KPIs, and compare entities through a cleaner dashboard.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if "uploaded_file_data" not in st.session_state:
    st.session_state.uploaded_file_data = None
if "selected_kpis" not in st.session_state:
    st.session_state.selected_kpis = None
if "chart_type" not in st.session_state:
    st.session_state.chart_type = "Metric Comparison"
if "metric_orientation" not in st.session_state:
    st.session_state.metric_orientation = "Vertical"
if "normalize_metrics" not in st.session_state:
    st.session_state.normalize_metrics = False

tab_upload, tab_local = st.sidebar.tabs(["Upload Dataset", "Local Files"])

loader = None
selected_file = None
data_source = None
dataset_id = None

with tab_upload:
    st.subheader("Upload CSV Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

    if uploaded_file is not None:
        try:
            uploaded_bytes = uploaded_file.getvalue()
            dataset_hash = hashlib.md5(uploaded_bytes).hexdigest()[:12]
            dataset_id = f"uploaded_{uploaded_file.name}_{dataset_hash}"

            with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp_file:
                tmp_file.write(uploaded_bytes)
                tmp_path = tmp_file.name

            loader = GenericDataLoader(tmp_path)
            selected_file = uploaded_file.name
            data_source = "uploaded"
            st.session_state.uploaded_file_data = tmp_path
            st.success(f"Loaded {uploaded_file.name}")
        except Exception as exc:
            st.error(f"Error loading file: {exc}")

with tab_local:
    st.subheader("Select Local Dataset")
    csv_files = [f for f in os.listdir(".") if f.endswith(".csv")]

    if csv_files:
        selected_local_file = st.selectbox("Select Dataset", csv_files)

        @st.cache_resource
        def load_local_data(csv_file):
            full_path = SCRIPT_DIR / csv_file
            return GenericDataLoader(str(full_path))

        if loader is None:
            try:
                selected_file = selected_local_file
                loader = load_local_data(selected_file)
                data_source = "local"
                dataset_id = f"local_{selected_file}"
            except Exception as exc:
                st.error(f"Error loading data: {exc}")
                st.stop()
        else:
            st.info("Using the uploaded dataset. Remove it to switch back to a local file.")
    else:
        st.info("No CSV files found in the current directory.")

if loader is None:
    st.warning("Upload a CSV file or select a local dataset to begin.")
    st.stop()


def init_analytics(_loader):
    return FlexibleAnalyticsEngine(_loader)


def init_visualizer(_loader, _analytics):
    return DynamicVisualizer(_loader, _analytics)


try:
    analytics = init_analytics(loader)
    visualizer = init_visualizer(loader, analytics)
except Exception as exc:
    st.error(f"Error initializing dashboard modules: {exc}")
    st.stop()

summary = loader.get_summary_stats()

with st.sidebar.expander("Dataset Profile", expanded=True):
    st.metric("Records", f"{summary['total_records']:,}")
    st.metric("Columns", summary["total_columns"])
    st.metric("Entities", len(summary["entities"]))
    st.caption(f"Entity column: `{summary['entity_column']}`")
    if summary["date_columns"]:
        st.caption(f"Date fields: {', '.join(summary['date_columns'][:2])}")

st.sidebar.divider()
st.sidebar.subheader("KPI Selection")
all_metrics = loader.numeric_columns
if all_metrics:
    selected_kpis = st.sidebar.multiselect(
        "Metrics to emphasize",
        all_metrics,
        default=all_metrics[: min(5, len(all_metrics))],
        key=f"kpi_select_{dataset_id}",
        help="These KPIs drive the core comparison views and the default charts.",
    )
    st.session_state.selected_kpis = selected_kpis if selected_kpis else all_metrics[:5]
else:
    st.session_state.selected_kpis = []
    st.sidebar.warning("No numeric columns were detected in this dataset.")

source_label = "Uploaded file" if data_source == "uploaded" else "Local file"
badge_html = "".join(
    [
        f'<span class="badge">{source_label}</span>',
        f'<span class="badge">{summary["total_records"]:,} rows</span>',
        f'<span class="badge">{len(summary["numeric_columns"])} numeric fields</span>',
        f'<span class="badge">{len(st.session_state.selected_kpis)} active KPIs</span>',
    ]
)
st.markdown(
    f"""
    <div class="hero-card">
        <div class="hero-kicker">Adaptive Analytics</div>
        <div class="hero-title">Flexible Comparison Dashboard</div>
        <div class="hero-copy">
            Explore <strong>{selected_file}</strong> with a sharper layout for entity comparison,
            metric storytelling, and chart-driven inspection.
        </div>
        <div class="badge-row">{badge_html}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

top_row = st.columns(4)
with top_row[0]:
    render_stat_card("Entity Axis", summary["entity_column"] or "Not found", "Primary comparison dimension")
with top_row[1]:
    render_stat_card("Metric Pool", str(len(summary["numeric_columns"])), "Detected numeric measures")
with top_row[2]:
    render_stat_card("Category Pool", str(len(summary["categorical_columns"])), "Detected categorical fields")
with top_row[3]:
    date_label = summary["date_columns"][0] if summary["date_columns"] else "Unavailable"
    render_stat_card("Time Field", date_label, "Trend analysis anchor")

entities = loader.get_all_entities()
if len(entities) < 2:
    st.warning(f"Need at least 2 entities to compare. Found {len(entities)}.")
    if entities:
        st.info(f"Detected entities: {', '.join(map(str, entities[:10]))}")
    st.stop()

render_section(
    "Comparison Setup",
    "Pick two different entities. The dashboard recalculates comparison tables, charts, trends, and insights from the same selection.",
)
selector_col1, selector_col2 = st.columns(2)
with selector_col1:
    entity1 = st.selectbox("Entity 1", entities, key="entity1")
with selector_col2:
    entity2 = st.selectbox("Entity 2", entities, key="entity2", index=1 if len(entities) > 1 else 0)

if entity1 == entity2:
    st.warning("Select two different entities to continue.")
    st.stop()

data1 = loader.get_entity_data(entity1)
data2 = loader.get_entity_data(entity2)
comparison = analytics.compare_entities(entity1, entity2)
metric_table = build_metric_table(comparison, entity1, entity2, st.session_state.selected_kpis)

tabs = st.tabs(["Overview", "Charts", "Metrics", "Trends", "Insights", "AI Optimization"])

with tabs[0]:
    render_section(
        "Executive Comparison",
        "Start with record volume, KPI leaders, and the most important summary deltas before drilling into category-level detail.",
    )
    overview_cols = st.columns(3)
    with overview_cols[0]:
        st.metric(entity1, f"{len(data1):,} records")
    with overview_cols[1]:
        st.metric("Selected KPIs", len(st.session_state.selected_kpis))
    with overview_cols[2]:
        st.metric(entity2, f"{len(data2):,} records")

    if not metric_table.empty:
        highlights = metric_table.reindex(metric_table["Difference"].abs().sort_values(ascending=False).index).head(3)
        lead_cols = st.columns(len(highlights)) if len(highlights) else []
        for idx, (_, row) in enumerate(highlights.iterrows()):
            with lead_cols[idx]:
                subtitle = f"{row['Leader']} leads by {format_value(abs(row['Difference']))}"
                render_stat_card(row["Metric"], format_value(max(row[entity1], row[entity2])), subtitle)

        st.markdown('<div class="section-label">Metric Table</div>', unsafe_allow_html=True)
        st.dataframe(style_metric_table(metric_table), use_container_width=True)
    else:
        st.info("No selected KPIs were available in the comparison output.")

    categorical_columns = [col for col in loader.categorical_columns if col != loader.entity_column]
    if categorical_columns:
        render_section(
            "Category Snapshots",
            "Review how the two entities distribute across the strongest categorical dimensions in the dataset.",
        )
        chosen_categories = categorical_columns[: min(2, len(categorical_columns))]
        for category in chosen_categories:
            category_cols = st.columns(2)
            with category_cols[0]:
                st.markdown(f"**{entity1} | {category}**")
                cat_df1 = (
                    data1[category].value_counts().head(8).rename_axis("Category").reset_index(name="Count")
                )
                st.dataframe(cat_df1, use_container_width=True, hide_index=True)
            with category_cols[1]:
                st.markdown(f"**{entity2} | {category}**")
                cat_df2 = (
                    data2[category].value_counts().head(8).rename_axis("Category").reset_index(name="Count")
                )
                st.dataframe(cat_df2, use_container_width=True, hide_index=True)

with tabs[1]:
    render_section(
        "Visual Explorer",
        "Switch between KPI, category, correlation, and compact dashboard views. Use quick buttons and comparison controls to reshape the charts live.",
    )
    preset_cols = st.columns(4)
    with preset_cols[0]:
        if st.button("KPI Bars", key="preset_metric"):
            st.session_state.chart_type = "Metric Comparison"
    with preset_cols[1]:
        if st.button("Category Donuts", key="preset_category"):
            st.session_state.chart_type = "Category Distribution"
    with preset_cols[2]:
        if st.button("Correlation Grid", key="preset_corr"):
            st.session_state.chart_type = "Correlation Matrix"
    with preset_cols[3]:
        if st.button("Mini Dashboard", key="preset_summary"):
            st.session_state.chart_type = "Summary Dashboard"

    chart_type = st.radio(
        "Chart Type",
        ["Metric Comparison", "Category Distribution", "Correlation Matrix", "Summary Dashboard"],
        horizontal=True,
        key="chart_type",
    )

    if chart_type == "Metric Comparison":
        if st.session_state.selected_kpis:
            control_cols = st.columns([1.3, 1, 1, 1])
            with control_cols[0]:
                selected_metrics = st.multiselect(
                    "Metrics to display",
                    st.session_state.selected_kpis,
                    default=st.session_state.selected_kpis[: min(4, len(st.session_state.selected_kpis))],
                )
            with control_cols[1]:
                metric_orientation = st.selectbox(
                    "Bar direction",
                    ["Vertical", "Horizontal"],
                    key="metric_orientation",
                )
            with control_cols[2]:
                normalize_metrics = st.toggle("Normalize values", key="normalize_metrics")
            with control_cols[3]:
                max_metric_count = min(8, len(st.session_state.selected_kpis))
                min_metric_count = 1 if max_metric_count < 3 else 3
                default_metric_count = min(4, max_metric_count)
                top_metric_count = st.slider("Show top", min_metric_count, max_metric_count, default_metric_count)

            if selected_metrics:
                if len(selected_metrics) > top_metric_count:
                    ranking_table = metric_table[metric_table["Metric"].isin(selected_metrics)].copy()
                    ranking_table["Magnitude"] = ranking_table["Difference"].abs()
                    selected_metrics = ranking_table.sort_values("Magnitude", ascending=False)["Metric"].head(top_metric_count).tolist()
                st.plotly_chart(
                    visualizer.plot_metric_comparison(
                        entity1,
                        entity2,
                        selected_metrics,
                        normalize=normalize_metrics,
                        orientation="h" if metric_orientation == "Horizontal" else "v",
                    ),
                    use_container_width=True,
                )
                st.caption("Tip: switch to horizontal mode when metric names are long, or normalize when scales are very different.")
    elif chart_type == "Category Distribution":
        if loader.categorical_columns:
            category_control_cols = st.columns([1.2, 1])
            with category_control_cols[0]:
                category_col = st.selectbox("Category", loader.categorical_columns)
            with category_control_cols[1]:
                max_categories = min(8, int(loader.df[category_col].nunique()))
                min_categories = 1 if max_categories < 4 else 4
                default_categories = min(6, max_categories)
                category_snapshot = st.slider(
                    "Categories to highlight",
                    min_categories,
                    max_categories,
                    default_categories,
                )
            chart_cols = st.columns(2)
            with chart_cols[0]:
                fig1 = visualizer.plot_category_distribution(category_col, entity1, top_n=category_snapshot)
                if fig1 is not None:
                    st.plotly_chart(fig1, use_container_width=True)
            with chart_cols[1]:
                fig2 = visualizer.plot_category_distribution(category_col, entity2, top_n=category_snapshot)
                if fig2 is not None:
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("No categorical columns found.")
    elif chart_type == "Correlation Matrix":
        chart_cols = st.columns(2)
        with chart_cols[0]:
            fig1 = visualizer.plot_correlation_heatmap(entity1)
            if fig1 is not None:
                st.plotly_chart(fig1, use_container_width=True)
        with chart_cols[1]:
            fig2 = visualizer.plot_correlation_heatmap(entity2)
            if fig2 is not None:
                st.plotly_chart(fig2, use_container_width=True)
    else:
        st.plotly_chart(visualizer.create_summary_dashboard(entity1, entity2), use_container_width=True)

with tabs[2]:
    render_section(
        "Metric Breakdown",
        "Inspect a single KPI with parallel descriptive statistics so the two entities are easy to compare without reading raw JSON.",
    )
    available_metrics = [metric for metric in loader.numeric_columns if metric in st.session_state.selected_kpis]
    if available_metrics:
        metric_col = st.selectbox("Metric", available_metrics)
        stats1 = analytics.get_entity_aggregates(entity1)[metric_col]
        stats2 = analytics.get_entity_aggregates(entity2)[metric_col]

        summary_cards = st.columns(3)
        with summary_cards[0]:
            leader = entity1 if stats1["sum"] > stats2["sum"] else entity2
            render_stat_card("Leader", leader, f"Highest total for {metric_col}")
        with summary_cards[1]:
            render_stat_card("Delta", format_value(abs(stats1["sum"] - stats2["sum"])), "Absolute sum difference")
        with summary_cards[2]:
            render_stat_card("Combined Count", f"{int(stats1['count'] + stats2['count']):,}", "Rows contributing to this KPI")

        stats_rows = [
            {"Statistic": "Sum", entity1: stats1["sum"], entity2: stats2["sum"]},
            {"Statistic": "Mean", entity1: stats1["mean"], entity2: stats2["mean"]},
            {"Statistic": "Median", entity1: stats1["median"], entity2: stats2["median"]},
            {"Statistic": "Min", entity1: stats1["min"], entity2: stats2["min"]},
            {"Statistic": "Max", entity1: stats1["max"], entity2: stats2["max"]},
            {"Statistic": "Std Dev", entity1: stats1["std"], entity2: stats2["std"]},
            {"Statistic": "Count", entity1: stats1["count"], entity2: stats2["count"]},
        ]
        stats_df = pd.DataFrame(stats_rows)
        styled_stats = stats_df.copy()
        for col in [entity1, entity2]:
            styled_stats[col] = styled_stats[col].map(format_value)
        st.dataframe(styled_stats, use_container_width=True, hide_index=True)
    else:
        st.warning("No selected KPIs found. Choose at least one metric in the sidebar.")

with tabs[3]:
    render_section(
        "Trend Watch",
        "Use a date field and aggregation frequency to contrast how the chosen KPI evolves across both entities over time.",
    )
    if loader.date_columns and st.session_state.selected_kpis:
        trend_cols = st.columns(3)
        with trend_cols[0]:
            metric = st.selectbox("Metric", st.session_state.selected_kpis, key="ts_metric")
        with trend_cols[1]:
            date_col = st.selectbox("Date Column", loader.date_columns, key="ts_date")
        with trend_cols[2]:
            frequency = st.selectbox(
                "Frequency",
                [("Daily", "D"), ("Weekly", "W"), ("Monthly", "M")],
                format_func=lambda x: x[0],
            )

        chart_cols = st.columns(2)
        with chart_cols[0]:
            fig1 = visualizer.plot_time_series(metric, entity1, frequency[1], date_col=date_col)
            if fig1 is not None:
                st.plotly_chart(fig1, use_container_width=True)
        with chart_cols[1]:
            fig2 = visualizer.plot_time_series(metric, entity2, frequency[1], date_col=date_col)
            if fig2 is not None:
                st.plotly_chart(fig2, use_container_width=True)
    else:
        if not loader.date_columns:
            st.info("No date columns found for time series analysis.")
        if not st.session_state.selected_kpis:
            st.warning("No selected KPIs found. Choose at least one metric in the sidebar.")

from ml_sales_optimizer import MLSalesOptimizer

with tabs[4]:
    render_section(
        "Insights And Raw Data",
        "Read the generated takeaways first, then drop into the underlying entity rows when you need validation or deeper inspection.",
    )
    insights = analytics.generate_insights(entity1, entity2)
    if insights:
        for insight in insights:
            render_insight(insight)
    else:
        st.markdown(
            '<div class="insight-empty">No major differences crossed the current significance thresholds.</div>',
            unsafe_allow_html=True,
        )

    if loader.categorical_columns and loader.numeric_columns:
        control_cols = st.columns(2)
        with control_cols[0]:
            category = st.selectbox("Top performer grouping", loader.categorical_columns, key="top_cat")
        with control_cols[1]:
            top_n = st.slider("Top N", 5, 20, 10)
        fig = visualizer.plot_top_performers(loader.numeric_columns[0], category, top_n)
        if fig is not None:
            st.plotly_chart(fig, use_container_width=True)

    data_view = st.radio("Raw Data View", ["Entity 1", "Entity 2", "Both"], horizontal=True)
    if data_view == "Entity 1":
        st.dataframe(data1, use_container_width=True, hide_index=True)
    elif data_view == "Entity 2":
        st.dataframe(data2, use_container_width=True, hide_index=True)
    else:
        raw_cols = st.columns(2)
        with raw_cols[0]:
            st.markdown(f"**{entity1}**")
            st.dataframe(data1, use_container_width=True, hide_index=True)
        with raw_cols[1]:
            st.markdown(f"**{entity2}**")
            st.dataframe(data2, use_container_width=True, hide_index=True)

with tabs[5]:
    render_section(
        "AI Optimization",
        "Forecast the chosen KPI and recommend a best price to maximize it using a lightweight ML model.",
    )

    if not st.session_state.selected_kpis:
        st.warning("Select at least one KPI in the sidebar first.")
    else:
        # Instantiate optimizer once
        optimizer = MLSalesOptimizer(loader, analytics)

        kpi = st.selectbox(
            "Target KPI (drives forecast + price recommendation)",
            st.session_state.selected_kpis,
            key="ai_kpi_select",
        )

        if not loader.date_columns:
            st.info("No date columns detected; skipping forecasting.")
        else:
            # Forecast controls
            freq_options = [("Daily", "D"), ("Weekly", "W"), ("Monthly", "M")]
            freq_label = st.selectbox(
                "Forecast frequency",
                freq_options,
                format_func=lambda x: x[0],
                key="ai_freq",
            )
            horizon_steps = st.slider("Forecast horizon (steps)", 1, 20, 8, key="ai_horizon")

            try:
                forecast = optimizer.forecast_target(
                    entity_name=entity1,
                    target_kpi=kpi,
                    date_col=None,
                    frequency=freq_label[1],
                    horizon_steps=horizon_steps,
                )

                import plotly.graph_objects as go

                # Plot last observed + forecast
                df_ent = loader.get_entity_data(entity1).copy()
                date_col = forecast.date_col
                df_ent[date_col] = pd.to_datetime(df_ent[date_col], errors="coerce")
                df_ent[kpi] = pd.to_numeric(df_ent[kpi], errors="coerce")
                df_ent = df_ent.dropna(subset=[date_col, kpi])

                hist = (
                    df_ent.groupby(pd.Grouper(key=date_col, freq=freq_label[1]))[kpi]
                    .mean()
                    .dropna()
                    .reset_index()
                    .rename(columns={kpi: "prediction"})
                )

                fig = go.Figure()
                fig.add_trace(
                    go.Scatter(
                        x=hist[date_col],
                        y=hist["prediction"],
                        mode="lines+markers",
                        name="History (mean)",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=forecast.forecast[date_col],
                        y=forecast.forecast["prediction"],
                        mode="lines+markers",
                        name="Forecast",
                    )
                )
                fig.update_layout(
                    title=f"{kpi} Forecast | {entity1}",
                    xaxis_title=date_col,
                    yaxis_title=kpi,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                st.plotly_chart(fig, use_container_width=True)

            except Exception as exc:
                st.error(f"Forecast failed: {exc}")

        # Price optimization
        st.markdown("---")
        st.subheader("Price Optimization (maximize chosen KPI)")

        if optimizer.price_col is None:
            st.warning("No `Price` column found in this dataset; skipping price optimization.")
        elif kpi not in loader.df.columns:
            st.warning("Chosen KPI column not found; skipping price optimization.")
        else:
            # Suggest bounds based on observed values
            df_ent = loader.get_entity_data(entity1).copy()
            df_ent[optimizer.price_col] = pd.to_numeric(df_ent[optimizer.price_col], errors="coerce")
            df_ent = df_ent.dropna(subset=[optimizer.price_col])
            if df_ent.empty:
                st.warning("No numeric Price data found for optimization.")
            else:
                p_min = float(df_ent[optimizer.price_col].min())
                p_max = float(df_ent[optimizer.price_col].max())

                col1, col2 = st.columns(2)
                with col1:
                    min_price = st.number_input("Min price", value=p_min, format="%.2f")
                with col2:
                    max_price = st.number_input("Max price", value=p_max, format="%.2f")

                if min_price < max_price:
                    try:
                        opt = optimizer.optimize_price(
                            entity_name=entity1,
                            target_kpi=kpi,
                            date_col=None,
                            min_price=min_price,
                            max_price=max_price,
                            grid_size=50,
                        )

                        uplift = opt.best_predicted_target - opt.baseline_predicted_target
                        uplift_pct = (uplift / opt.baseline_predicted_target * 100) if opt.baseline_predicted_target else 0

                        left, right = st.columns(2)
                        with left:
                            render_stat_card("Best Price", f"{opt.best_price:.2f}", "Within observed bounds")
                            render_stat_card("Predicted KPI", format_value(opt.best_predicted_target), "At best price")
                        with right:
                            render_stat_card("Baseline KPI", format_value(opt.baseline_predicted_target), "At median observed price")
                            render_stat_card(
                                "Uplift",
                                f"{uplift:+.2f} ({uplift_pct:+.1f}%)",
                                "Predicted improvement vs baseline",
                            )

                        st.caption(
                            "Model: linear regression using Price and time trend. For real pricing, validate experimentally."
                        )

                    except Exception as exc:
                        st.error(f"Price optimization failed: {exc}")
                else:
                    st.warning("Min price must be less than max price.")

st.divider()
st.markdown(
    """
    <div class="footer-note">
        This interface adapts to any CSV dataset by detecting the entity axis, KPI candidates, date fields, and category structure automatically.
    </div>
    """,
    unsafe_allow_html=True,
)
