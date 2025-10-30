import streamlit as st
import pandas as pd
import altair as alt
from utils import load_data

st.header("EDA Gallery")

st.markdown("Upload or link your dataset, then explore four distinct chart types with brief explainers.")

src = st.radio("Data source", ["Local CSV (data/vgsales.csv)", "CSV URL"], horizontal=True)
url = st.text_input("CSV URL") if src == "CSV URL" else None
local_default = "data/vgsales.csv" # change filename if needed

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

#Defaults tailored for vgsales.csv but user can change
num = st.selectbox("Numeric column (for hist/box)", numeric_cols, index=(numeric_cols.index('global_sales') if 'global_sales' in numeric_cols else 0))
cat = st.selectbox("Category column (for bar/box)", cat_cols, index=(cat_cols.index('genre') if 'genre' in cat_cols else 0))

st.subheader("1) Histogram")
st.caption("How to read: x = values of the numeric column; y = count. Look for skew/outliers.")
hist = alt.Chart(df).mark_bar().encode(
  x=alt.X(f"{num}:Q", bin=alt.Bin(maxbins=30)),
  y='count()',
  tooltip=['count()']
)
st.altair_chart(hist.properties(height=320), use_container_width=True)

st.subheader("2) Bar by Category (mean of numeric)")
st.caption("How to read: bar height = average of the numeric column for each category; compare across bars.")
bar = alt.Chart(df).mark_bar().encode(
  x=alt.X(f"{cat}:N", sort='-y'),
  y=alt.Y(f"mean({num}):Q"),
  tooltip=[cat, alt.Tooltip(f"mean({num}):Q", title="Mean")]
)
st.altair_chart(bar.properties(height=320), use_container_width=True)


st.subheader("3) Scatter Plot (numeric vs numeric)")
num2 = st.selectbox("Second numeric for scatter", [c for c in numeric_cols if c != num]) if len(numeric_cols) > 1 else None
if num2:
  st.caption("How to read: each point is a row; patterns imply relationships or clusters.")
  scat = alt.Chart(df).mark_circle().encode(
    x=f"{num}:Q",
    y=f"{num2}:Q",
    tooltip=list(df.columns)[:6]
  ).interactive()
  st.altair_chart(scat.properties(height=320), use_container_width=True)
else:
  st.info("Select a second numeric column to enable the scatter plot.")


st.subheader("4) Box Plot by Category")
st.caption("How to read: box shows distribution (median/IQR) of the numeric column per category; dots are outliers.")
box = alt.Chart(df).mark_boxplot().encode(
  x=f"{cat}:N",
  y=f"{num}:Q",
  tooltip=[cat, num]
)
st.altair_chart(box.properties(height=320), use_container_width=True)


st.markdown("**Observations (write a few bullets below):**")
st.text_area("Notes", "- …", height=120)
