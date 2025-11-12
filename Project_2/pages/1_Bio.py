import streamlit as st

st.title("Professional Bio")

img_path = Path("assets/IMG_2154.jpg")
if img_path.exists():
    st.image(str(img_path), caption="Caiden Kopcik", use_column_width=True)
else:
    st.warning(f"Image not found at {img_path}")

st.markdown("""
**Caiden Kopcik**

Hello!
-  I am a full-stack developer, and data visulization student at Metropolitan State University of Denver. 
  My current job is to make interactive dashboards and analytics solutions that employ stuff like Python and Streamlit together.
  I have found more interest in transforming raw data/datasets into clear, accessible visuals that tell stories and help with real world decision(s).
""")

st.subheader("Highlights")
st.markdown("""
- I have obtained experienced with languages/tools like Python, Pandas, Plotly, Streamlit, etc. 
- I Know the use of cloud tools, such as, AWS, Terraform, Azure IoT 
- I am Skilled in data wrangling, dashboards, and machine learning pipelines  
- Building academic/professional portfolio(s) focused more on data analytics

""")

st.subheader("My Visualization Approach")
st.markdown("""
I try to design visualizations so that they are more clear, inclusive, and data-driven.  
That means things like color-blind–safe palettes, labeled axes, and transparent communication of uncertainty.  
Good visualization should help everyone explore insights, and not overwhelm them with noise.

""")
