import streamlit as st
from yfiles_graphs_for_streamlit import GraphComponent

nodes = [
    {"id": 0, "properties": {"firstName": "Alpha", "label": "Person A"}, "size": (110,110), "color": '#AC94F4', 'coordinates': [48.522, 9.0522]},
    {"id": "one", "properties": {"firstName": "Bravo", "label": "Person B"},"color": "purple", 'heat': 0.7},
    {"id": 2.0, "properties": {"firstName": "Charlie", "label": "Person C", "has_hat": False}, "color": "violet", 'heat': 0.3},
    {"id": True, "properties": {"firstName": "Delta", "label": "Person D", "likes_pizza": True},"color": "#DE73FF", 'heat': 0.5}
]
edges = [
    {"id": "zero", "start": 0, "end": "one", "properties": {"since": "1992", "label": "knows"}, "color": "#C64B8C"},
    {"id": 1, "start": "one", "end": True, "properties": {"label": "knows", "since": "1992"}, "color": "#C64B8C"},
    {"id": 2.0, "start": 2.0, "end": True, "properties": {"label": "knows", "since": "1992"}, "color": "#C64B8C"},
    {"id": False, "start": 0, "end": 2.0, "properties": {"label": "knows", "since": 234}, "color": "#C64B8C"}
]
directed = True

st.set_page_config(
    page_title="YWorks Streamlit Component",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("---")

#container = st.container()
st.title("Introduction")
one = GraphComponent(nodes, edges, directed)
st.markdown("---")
