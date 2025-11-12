import streamlit as st
import pandas as pd
import altair as alt

try:
    from utils import load_data
except Exception:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from utils import load_data

st.header("EDA Gallery")
st.markdown("Upload or link your dataset, then explore four distinct chart types with brief explainers.")

src = st.radio("Data source", ["Local CSV (data/vgsales.csv)", "CSV URL"], horizontal=True)
url = st.text_input("CSV URL") if src == "CSV URL" else None
local_default = "data/vgsales.csv"  # change filename if needed

df = load_data(local_default if src.startswith("Local") else None, url)

if df.empty:
    st.warning("No data loaded yet. Place a CSV in data/ or paste a URL above.")
    st.stop()

st.write("**Shape:**", df.shape)
with st.expander("Preview first rows"):
    st.dataframe(df.head(), use_container_width=True)

numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
cat_cols = [c for c in df.columns if df[c].dtype == 'object']

if not numeric_cols or not cat_cols:
    st.info("For best results, include at least one numeric and one categorical column.")

# Defaults tailored for vgsales.csv but user can change
num_default_index = numeric_cols.index('global_sales') if 'global_sales' in numeric_cols else 0
cat_default_index = cat_cols.index('genre') if 'genre' in cat_cols else 0

num = st.selectbox("Numeric column (for hist/box)", numeric_cols, index=num_default_index)
cat = st.selectbox("Category column (for bar/box)", cat_cols, index=cat_default_index)

# 1) Histogram
st.subheader("1) Histogram")
st.text_input("Question explored (Histogram)", f"What does the distribution of {num} look like?", key="q_hist")
st.caption("How to read: x = values of the numeric column; y = count. Look for skew/outliers.")
hist = alt.Chart(df).mark_bar().encode(
    x=alt.X(f"{num}:Q", bin=alt.Bin(maxbins=30), title=num),
    y=alt.Y('count()', title='Count'),
    tooltip=['count()']
).interactive()
st.altair_chart(hist.properties(height=320), use_container_width=True)
st.caption("Source: Zenodo Video Games Sales · Units in millions")
st.markdown("**Observation(s):**")
st.text_area("Obs - Histogram", "- The distribution of global_sales is strongly right-skewed.", height=80, key="obs_hist")

# 2) Bar by Category
st.subheader("2) Bar by Category (mean of numeric)")
st.text_input("Question explored (Bar)", f"Which {cat} has the highest average {num}?", key="q_bar")
st.caption("How to read: bar height = average of the numeric column for each category; compare across bars.")
bar = alt.Chart(df).mark_bar().encode(
    x=alt.X(f"{cat}:N", sort='-y', title=cat),
    y=alt.Y(f"mean({num}):Q", title=f"Mean {num}"),
    tooltip=[cat, alt.Tooltip(f"mean({num}):Q", title="Mean")]
).interactive()
st.altair_chart(bar.properties(height=320), use_container_width=True)
st.caption("Source: Zenodo Video Games Sales · Units in millions")
st.markdown("**Observation(s):**")
st.text_area("Obs - Bar", "- Sports and Platform genres tend to have higher mean sales than Strategy/Adventure.", height=80, key="obs_bar")

# 3) Scatter
st.subheader("3) Scatter Plot (numeric vs numeric)")
num2_candidates = [c for c in numeric_cols if c != num]
num2 = st.selectbox("Second numeric for scatter", num2_candidates) if len(num2_candidates) else None
if num2:
    st.text_input("Question explored (Scatter)", f"Is {num} related to {num2}?", key="q_scatter")
    st.caption("How to read: each point is a row; patterns imply relationships or clusters.")
    scat = alt.Chart(df).mark_circle().encode(
        x=alt.X(f"{num}:Q", title=num),
        y=alt.Y(f"{num2}:Q", title=num2),
        tooltip=list(df.columns)[:6]
    ).interactive()
    st.altair_chart(scat.properties(height=320), use_container_width=True)
    st.caption("Source: Zenodo Video Games Sales · Units in millions")
    st.markdown("**Observation(s):**")
    st.text_area("Obs - Scatter", "- There is an inverse relationship between rank and global_sales.", height=80, key="obs_scatter")
else:
    st.info("Select a second numeric column to enable the scatter plot.")

# 4) Box Plot
st.subheader("4) Box Plot by Category")
st.text_input("Question explored (Box)", f"How does the distribution of {num} vary by {cat}?", key="q_box")
st.caption("How to read: box shows distribution (median/IQR) of the numeric column per category; dots are outliers.")
box = alt.Chart(df).mark_boxplot().encode(
    x=alt.X(f"{cat}:N", title=cat),
    y=alt.Y(f"{num}:Q", title=num),
    tooltip=[cat, num]
)
st.altair_chart(box.properties(height=320), use_container_width=True)
st.caption("Source: Zenodo Video Games Sales · Units in millions")
st.markdown("**Observation(s):**")
st.text_area("Obs - Box", "- Action and Sports categories show the widest spread in sales (largest IQR).", height=80, key="obs_box")

# (Optional) Keep your overall notes area if you like
st.markdown("**Overall Notes (optional, 3–6 bullets):**")
st.text_area(
    "Notes",
    "- Most games sell under 1M units; a few blockbusters dominate totals.\n"
    "- Genre and platform choices strongly influence average sales.\n"
    "- Right-skewed distribution implies long-tail dynamics in the market.\n",
    height=120
)
