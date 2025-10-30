import streamlit as st

st.header("Professional Bio")

st.write(
  """
**Your Name**
_(Replace this section with your 3–6 sentence professional summary.)_
  
**Highlights (3–5 bullets):**
- _(Add tools/skills here)_
- _(Add coursework/projects)_

**Visualization philosophy:**
_(1–2 sentences on clarity, accessibility, ethics.)_
"""
)

with st.expander("Optional: Profile Image + Alt‑text"):
  st.caption("Add `assets/profile.jpg` and describe it briefly below.")
# st.image("assets/profile.jpg", use_column_width=True, caption="Alt: headshot of student ...")
