import streamlit as st

st.header("🧭 Future Work")

st.markdown("""
Below this should be several steps that could expand or refine this analytics project in the future.  
I want to focus on making things more interactive, easier to use, and giving more detailed data insights.
""")

st.subheader("📈 Future Improvements & Extensions")
st.markdown("""
- Add a **100% stacked bar chart** to compare **regional sales shares** by genre or platform.  
- Introduce a "heatmap" of maybe "platform x genre" to visualize performance patterns.  
- Smoother year trends with a "moving average" to reduce yearly variance noise.  
- Run a possible "accessibility audit" for things like color contrast, alt text, keyboard navigation, screen reader labels, etc.  
- Enrich the dataset with "critic and user scores" to compare sales vs. reception (descriptive only).  
- Integrate with an "API" for updated video game data in future dashboards.  
""")

st.subheader("🪶 Reflection (What Changed from Lab 4.3 Prototype)")
st.markdown("""
- Consolidated filters into a more consistent and reusable layout on the Dashboard page.  
- Added clearer axis labels, stronger contrast, and alt-text for improved accessibility.  
- Included “How to Read This Chart” explainers in the EDA Gallery for each visualization.  
- Improved interactive behavior: hover tooltips, dynamic updates, and smoother layout.  
- Enhanced color palette for readability across light and dark modes.  
""")
