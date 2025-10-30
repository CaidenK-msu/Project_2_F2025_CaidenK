from __future__ import annotations
import pandas as pd
import streamlit as st
from pathlib import Path


@st.cache_data(show_spinner=False)
def load_data(local_path: str | None = None, url: str | None = None) -> pd.DataFrame:
"""Load CSV from local path or URL with light standardization.
Returns empty DataFrame on failure so pages can guard gracefully.
"""
try:
if local_path and Path(local_path).exists():
df = pd.read_csv(local_path)
elif url:
df = pd.read_csv(url)
else:
return pd.DataFrame()
# Normalize column names
df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
return df
except Exception as e:
st.warning(f"Could not load data: {e}")
return pd.DataFrame()




def kpis(df: pd.DataFrame, numeric_col: str | None = None, category_col: str | None = None):
"""Compute simple KPIs for dashboard tiles."""
return {
"rows": int(len(df)),
"columns": int(len(df.columns)),
"distinct_categories": int(df[category_col].nunique()) if category_col and category_col in df else None,
"mean_value": float(df[numeric_col].mean()) if numeric_col and numeric_col in df else None,
"median_value": float(df[numeric_col].median()) if numeric_col and numeric_col in df else None,
"latest_refresh": pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
}
