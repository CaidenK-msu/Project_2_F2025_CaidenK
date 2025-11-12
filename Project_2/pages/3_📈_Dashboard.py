import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data, kpis

st.subheader("Filters")

selected_cats = st.multiselect(
    "Filter categories",
    sorted(df[cat].dropna().unique().tolist())[:50]
)
if selected_cats:
    df = df[df[cat].isin(selected_cats)]

num_min = float(df[num].min())
num_max = float(df[num].max())
rng = st.slider(
    f"Filter by {num} range",
    min_value=num_min,
    max_value=num_max,
    value=(num_min, num_max)
)
df = df[df[num].between(rng[0], rng[1])]

st.subheader("KPIs")
metrics = kpis(df, numeric_col=num, category_col=cat)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Rows", metrics["rows"])
col2.metric("Distinct categories", metrics["distinct_categories"])
col3.metric("Mean", f"{metrics['mean_value']:.2f}" if metrics['mean_value'] is not None else "—")
col4.metric("Median", f"{metrics['median_value']:.2f}" if metrics['median_value'] is not None else "—")
st.caption(f"Last refreshed: {metrics['latest_refresh']}")

left, right = st.columns(2)
with left:
    st.markdown("**Bar: mean by category**")
    bar = alt.Chart(df).mark_bar().encode(
        x=alt.X(f"{cat}:N", sort='-y', title=cat),
        y=alt.Y(f"mean({num}):Q", title=f"Mean {num}"),
        tooltip=[cat, alt.Tooltip(f"mean({num}):Q", title="Mean")]
    ).properties(height=360)
    st.altair_chart(bar, use_container_width=True)

with right:
    st.markdown("**Histogram: distribution of numeric**")
    hist = alt.Chart(df).mark_bar().encode(
        x=alt.X(f"{num}:Q", bin=alt.Bin(maxbins=30), title=num),
        y=alt.Y('count()', title='Count'),
        tooltip=['count()']
    ).properties(height=360)
    st.altair_chart(hist, use_container_width=True)

st.subheader("Narrative Insights (3–6 bullets)")
try:
    by_cat = df.groupby(cat, dropna=False)[num].mean().sort_values(ascending=False)
    top_cat = by_cat.index[0] if len(by_cat) else None
    insight_lines = [
        f"- **Top {cat} by mean {num}**: {top_cat} ({by_cat.iloc[0]:.2f})" if top_cat is not None else "- Not enough data to compute category means.",
        f"- **Rows after filters**: {len(df)} across **{df[cat].nunique()}** {cat} groups.",
        f"- **Central tendency**: mean {num} = {df[num].mean():.2f}, median = {df[num].median():.2f}.",
    ]
except Exception:
    insight_lines = ["- Add filters to see insights."]

preset = "\n".join(insight_lines + ["- …", "- …"])
st.text_area("Notes (edit as needed)", preset, height=160)

st.subheader("Reproducibility")
st.write("**Data source:** Zenodo Video Games Sales (https://zenodo.org/records/5898311)")
st.write("**Last refreshed:** See KPI timestamp above.")

