import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Mini Analytics Portfolio", page_icon="📚", layout="wide")

st.title("Welcome!")
st.write(
    "Use the **sidebar** to navigate the app pages:\n"
    "- **Bio**\n"
    "- **Charts Gallery**\n"
    "- **Dashboard**\n"
    "- **Future Work**"
)

st.caption(
    "Tip: Start with the **Charts Gallery** to explore columns, then use the **Dashboard** for filters + KPIs."
)


