import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Node, Edge

st.set_page_config(
    page_title="yFiles Graphs for Streamlit",
    layout="wide"
)

st.markdown("---")
st.title("Introduction")

# Structured sample data.
# - Each node must provide an id property
# - Each edge must provide an id, start and end property that resolve to the node ids to form the graph structure.
# - Optionally, provide additional properties in a "properties" property.
nodes = [
    Node(id=0, properties={"firstName": "Alpha", "label": "Person A"}),
    Node(id=1, properties={"firstName": "Bravo", "label": "Person B"}),
    Node(id=2, properties={"firstName": "Charlie", "label": "Person C", "has_hat": False}),
    Node(id=3, properties={"firstName": "Delta", "label": "Person D", "likes_pizza": True})
]
edges = [
    Edge(start=0, end=1, properties={"since": "1992", "label": "knows"}),
    Edge(start=1, end=3, properties={"label": "knows", "since": "1992"}),
    Edge(start=2, end=3, properties={"label": "knows", "since": "1992"}),
    Edge(start=0, end=2, properties={"label": "knows", "since": 234})
]

# initialize and render the component
StreamlitGraphWidget(nodes, edges).show()

st.markdown("---")
