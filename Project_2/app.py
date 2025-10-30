import streamlit as st
from pathlib import Path


st.set_page_config(page_title="Mini Analytics Portfolio", page_icon="📚", layout="wide")


#Brand header
col1, col2 = st.columns([1,6])
with col1:
  if Path("assets/logo.png").exists():
    st.image("assets/logo.png", width=84, caption="Alt: project logo")
with col2:
  st.title("Mini Analytics Portfolio")
  st.caption("Bio • EDA Gallery • Dashboard • Future Work")

st.markdown(
  """
  This multipage Streamlit app showcases exploratory data analysis and a small dashboard on a dataset with more than 100 rows.
  **Navigation**: Use the left sidebar.
  **Data**: Place a CSV in `data/` (e.g., `vgsales.csv`) or paste a CSV URL on the pages.
  
  
  **Accessibility**: We aim for color‑blind‑safe palettes, labeled axes/units, and concise alt‑text.
  """
)

st.info("Tip: Start with the **EDA Gallery** to explore columns, then use the **Dashboard** for filters + KPIs.")
