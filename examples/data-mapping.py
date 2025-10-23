import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget
from networkx import erdos_renyi_graph

st.set_page_config(
    page_title="yFiles Graphs for Streamlit",
    layout="wide",
)

st.markdown("---")
st.title("Data-driven visualization")

# import NetworkX sample graph
graph = StreamlitGraphWidget.from_graph(erdos_renyi_graph(10, 0.3, 2))

# map each node to a fixed color
graph.set_node_color_mapping(lambda node: '#00BCD4')

# change the node size
graph.set_node_size_mapping(lambda index, node: (55 + 10 * (index % 5), 55 - 10 * (index % 5)))

# apply a heat mapping
graph.set_heat_mapping(lambda element: 0.5 if element['id'] % 2 == 0 else 0.0)

# render the component
graph.show()

st.markdown("---")
