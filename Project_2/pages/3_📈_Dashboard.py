import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data, kpis

st.header("Interactive Dashboard")

src = st.radio("Data source", ["Local CSV (data/vgsales.csv)", "CSV URL"], horizontal=True)
url = st.text_input("CSV URL") if src == "CSV URL" else None
local_default = "data/vgsales.csv"

with st.spinner("Loading data…"):
    df = load_data(local_default if src.startswith("Local") else None, url)

if df.empty:
    st.warning("No data loaded. Add a CSV to data/ or paste a URL above.")
    st.stop()

st.subheader("Setup your fields")
cat_options = [c for c in df.columns if df[c].dtype == 'object']
num_options = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

cat_default = cat_options.index('platform') if 'platform' in cat_options else 0
num_default = num_options.index('global_sales') if 'global_sales' in num_options else 0

cat = st.selectbox("Primary category", cat_options, index=cat_default)
num = st.selectbox("Primary numeric", num_options, index=num_default)

# ---------- Robust optional datetime handling ----------
time_candidates = []
for c in df.columns:
    s = pd.to_datetime(df[c], errors="coerce", utc=True)
    if s.notna().mean() >= 0.60:
        time_candidates.append(c)

time_col = st.selectbox("Optional date/time column", ["(none)"] + time_candidates)

time_mask = None
if time_col != "(none)":
    s = pd.to_datetime(df[time_col], errors="coerce", utc=True)
    valid = s.dropna()
    if valid.empty:
        st.info("Selected time column doesn't contain valid dates; date filter disabled.")
    else:
        min_d = valid.min().to_pydatetime()
        max_d = valid.max().to_pydatetime()
        if min_d == max_d:
            st.info("Date column has only one unique timestamp; range filter skipped.")
        else:
            date_range = st.slider("Date range", min_value=min_d, max_value=max_d, value=(min_d, max_d))
            start, end = pd.Timestamp(date_range[0], tz="UTC"), pd.Timestamp(date_range[1], tz="UTC")
            time_mask = s.between(start, end)
            
# -------------------------------------------------------------------------

st.subheader("Filters")
selected_cats = st.multiselect("Filter categories", sorted(df[cat].dropna().unique().tolist())[:50])
if selected_cats:
    df = df[df[cat].isin(selected_cats)]
if time_mask is not None:
    df = df[time_mask]

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
        x=alt.X(f"{cat}:N", sort='-y'),
        y=alt.Y(f"mean({num}):Q"),
        tooltip=[cat, alt.Tooltip(f"mean({num}):Q", title="Mean")]
    ).properties(height=360)
    st.altair_chart(bar, use_container_width=True)

with right:
    st.markdown("**Histogram: distribution of numeric**")
    hist = alt.Chart(df).mark_bar().encode(
        x=alt.X(f"{num}:Q", bin=alt.Bin(maxbins=30)),
        y='count()',
        tooltip=['count()']
    ).properties(height=360)
    st.altair_chart(hist, use_container_width=True)

st.subheader("Narrative Insights (3–6 bullets)")
st.text_area("Notes", "- …\n- …", height=140)

st.subheader("Reproducibility")
st.write("**Data source:** Zenodo Video Games Sales (https://zenodo.org/records/5898311)")
st.write("**Last refreshed:** See KPI timestamp above.")
