import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout
from networkx import erdos_renyi_graph

st.set_page_config(
    page_title="yFiles Graphs for Streamlit",
    layout="wide",
)
st.title("Select some nodes or edges")

# caching is important here to not lose track of the component"s reference when populating the page"s input fields
@st.cache_resource
def component_creator():
    return StreamlitGraphWidget.from_graph(erdos_renyi_graph(10, 0.3, 2))

graph = component_creator()
graph.node_size_mapping = lambda index, node: (55 + 10 * (index % 5), 55 - 10 * (index % 5))

# get the selected nodes and edges from the component with sync_selection=True
selected_nodes, selected_edges = graph.show(sync_selection=True)
st.write("Selected Edges: ", ", ".join(str(edge["id"]) for edge in selected_edges))
st.write("Selected Nodes: ", ", ".join(str(edge["id"]) for edge in selected_nodes))

st.markdown("---")
st.title("Another component")

# get the selected nodes and edges from the component with sync_selection=True
selected_nodes, selected_edges = graph.show(sync_selection=True, graph_layout=Layout.HIERARCHIC, key="2nd component")
st.write("Selected Edges: ", ", ".join(str(edge["id"]) for edge in selected_edges))
st.write("Selected Nodes: ", ", ".join(str(edge["id"]) for edge in selected_nodes))