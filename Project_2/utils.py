from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def load_data(local_path: str | None = None, url: str | None = None) -> pd.DataFrame:
    """
    Load CSV from local path or URL (with light standardization).
    Should try a couple of locations so it works both locally and on a Streamlit Cloud.
    Will return an empty DataFrame on failure so pages can guard gracefully.
    """
    try:
        if local_path:
            p = Path(local_path)
            if not p.exists():
                p = Path(__file__).resolve().parent / local_path
            if not p.exists():
                return pd.DataFrame()
            df = pd.read_csv(p)
        elif url:
            df = pd.read_csv(url)
        else:
            return pd.DataFrame()
        df.columns = [c.strip().replace(" ", "_").lower() for c in df.columns]
        return df

    except Exception as e:
        st.warning(f"Could not load data: {e}")
        return pd.DataFrame()


def kpis(
    df: pd.DataFrame,
    numeric_col: str | None = None,
    category_col: str | None = None,
) -> dict:
    """Compute simple KPIs for dashboard tiles."""
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "distinct_categories": int(df[category_col].nunique()) if category_col and category_col in df else None,
        "mean_value": float(df[numeric_col].mean()) if numeric_col and numeric_col in df else None,
        "median_value": float(df[numeric_col].median()) if numeric_col and numeric_col in df else None,
        "latest_refresh": pd.Timestamp.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
    }
