import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget

st.set_page_config(
    page_title="yFiles Graphs for Streamlit",
    layout="wide"
)

st.markdown("---")
st.title("Introduction")

# Structured sample data.
# - Each node dict must provide an id property
# - Each edge dict must provide an id, start and end property that resolve to the node ids to form the graph structure.
# - Optionally, provide additional properties in a "properties" property.
nodes = [
    {"id": 0, "properties": {"firstName": "Alpha", "label": "Person A"}},
    {"id": 1, "properties": {"firstName": "Bravo", "label": "Person B"}},
    {"id": 2, "properties": {"firstName": "Charlie", "label": "Person C", "has_hat": False}},
    {"id": 3, "properties": {"firstName": "Delta", "label": "Person D", "likes_pizza": True}}
]
edges = [
    {"id": 0, "start": 0, "end": 1, "properties": {"since": "1992", "label": "knows"}},
    {"id": 1, "start": 1, "end": 3, "properties": {"label": "knows", "since": "1992"}},
    {"id": 2, "start": 2, "end": 3, "properties": {"label": "knows", "since": "1992"}},
    {"id": 3, "start": 0, "end": 2, "properties": {"label": "knows", "since": 234}}
]

# initialize and render the component
StreamlitGraphWidget(nodes, edges).show()

st.markdown("---")
