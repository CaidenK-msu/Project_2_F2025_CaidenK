import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities

def build_friendship_graph():
    nodes = ["Alice", "Bob", "Charlie", "Diana", "Eve",
             "Frank", "Grace", "Hannah", "Ian", "Jack"]

    edges = [
        ("Alice", "Bob"),
        ("Alice", "Charlie"),
        ("Bob", "Charlie"),
        ("Charlie", "Diana"),
        ("Diana", "Eve"),
        ("Bob", "Diana"),
        ("Frank", "Eve"),
        ("Eve", "Ian"),
        ("Diana", "Ian"),
        ("Ian", "Grace"),
        ("Grace", "Hannah"),
        ("Hannah", "Jack"),
        ("Grace", "Jack"),
        ("Charlie", "Frank"),
        ("Alice", "Eve"),
        ("Bob", "Jack"),
    ]

    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Make layout consistent
    pos = nx.spring_layout(G, seed=42)
    return G, pos

st.title("Lab 6.1 – Network Visualization & Analysis")
st.caption("Friendship Network in a College Class")

st.write(
    """
This page contains the full network analysis from Lab 6.1,
including network visualization, centrality metrics,
community detection, and identification of the most influential student.
"""
)

G, pos = build_friendship_graph()

st.subheader("1. Network Visualization")

fig1, ax1 = plt.subplots(figsize=(6, 4))
nx.draw(
    G, pos, ax=ax1,
    with_labels=True,
    node_color="skyblue",
    node_size=1200,
    font_size=10,
)
ax1.set_title("Friendship Network")
st.pyplot(fig1)

st.subheader("2. Centrality Measures")

degree = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)
eigen = nx.eigenvector_centrality(G, max_iter=500)

centrality_df = pd.DataFrame({
    "Node": list(G.nodes()),
    "Degree": [degree[n] for n in G.nodes()],
    "Betweenness": [betweenness[n] for n in G.nodes()],
    "Closeness": [closeness[n] for n in G.nodes()],
    "Eigenvector": [eigen[n] for n in G.nodes()],
}).set_index("Node").round(3)

st.dataframe(centrality_df)

# Identify top students
most_connected = max(degree, key=degree.get)
top_betweenness = max(betweenness, key=betweenness.get)
top_closeness = max(closeness, key=closeness.get)
most_influential = max(eigen, key=eigen.get)

st.markdown(
    f"""
**Most connected (Degree):** `{most_connected}`  
**Highest Betweenness (Bridge):** `{top_betweenness}`  
**Highest Closeness (Best Positioned):** `{top_closeness}`  
**Most Influential (Eigenvector):** `{most_influential}`  
"""
)

st.subheader("3. Community Detection")

communities = list(greedy_modularity_communities(G))

st.write("Detected Communities:")
for i, c in enumerate(communities, 1):
    st.write(f"- **Community {i}:** {', '.join(sorted(c))}")

st.subheader("4. Highlighted Most Influential Student")

colors = ["red" if n == most_influential else "skyblue" for n in G.nodes()]

fig2, ax2 = plt.subplots(figsize=(6, 4))
nx.draw(
    G, pos, ax=ax2,
    with_labels=True,
    node_color=colors,
    node_size=1400,
    font_size=10,
)
ax2.set_title(f"Most Influential Student: {most_influential}")
st.pyplot(fig2)

st.subheader("5. Findings Summary")

st.markdown(
    f"""
- The network includes **{G.number_of_nodes()} students** and **{G.number_of_edges()} friendship connections**.
- **{most_connected}** is the most connected student (highest degree).
- **{top_betweenness}** acts as the main bridge between groups.
- **{top_closeness}** can reach all students the fastest.
- **{most_influential}** is the most influential student based on eigenvector centrality.
"""
)

#Ressource(s) used for help
# ChatGPT  
#  https://chatgpt.com/ 
