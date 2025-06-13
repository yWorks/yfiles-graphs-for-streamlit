import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget
from networkx import erdos_renyi_graph

g = erdos_renyi_graph(10, 0.3, 2)

graph = StreamlitGraphWidget.from_graph(g)
graph.set_node_color_mapping(lambda node: '#e1c4ff')
graph.set_node_size_mapping(lambda index, node: (55 + 10 * (index % 5), 55 - 10 * (index % 5)))
graph.set_heat_mapping(lambda element: 0.5 if element['id'] % 2 == 0 else 0.0)

st.set_page_config(
    page_title="yFiles Graphs for Streamlit",
    layout="wide",
)

st.markdown("---")

st.title("Introduction")
graph.show()

st.markdown("---")

st.title('Another Component') # TODO show different data mapping options
graph.set_node_color_mapping(lambda node: 'red')
graph.edges = []
graph.show(key="foobar")
