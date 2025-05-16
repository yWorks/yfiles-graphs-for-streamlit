import streamlit as st
from yfiles_graphs_for_streamlit import GraphComponent
from networkx import erdos_renyi_graph

g = erdos_renyi_graph(10, 0.3, 2)
directed = True

component = GraphComponent()
component.import_graph(g)
component.set_node_color_mapping(lambda node: '#e1c4ff')
component.set_node_size_mapping(lambda index, node: (55 + 10 * (index % 5), 55 - 10 * (index % 5)))
component.set_heat_mapping(lambda element: 0.5 if element['id'] % 2 == 0 else 0.0)
nodes = component.nodes
edges = component.edges

st.set_page_config(
    page_title="YWorks Streamlit Component",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("---")

#container = st.container()
st.title("Introduction")
component(nodes, edges, directed)

st.markdown("---")
