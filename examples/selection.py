import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout, EdgeStyle
from networkx import florentine_families_graph

st.set_page_config(
    page_title="yFiles Graphs for Streamlit",
    layout="wide",
)
st.title("Select some nodes or edges")

# the Medici marriage line
medici_line = ["Acciaiuoli", "Medici", "Albizzi", "Guadagni", "Lamberteschi"]

def is_in_medici_line(node_id: int) -> bool:
    """Return True if the node represents a Medici marriage line node"""
    for node in graph.nodes:
        if node.get("id") == node_id:
            label = (
                    node.get("properties", {}).get("label")
                    or node.get("label")  # fallback if properties.label missing
            )
            return label in medici_line if label is not None else False
    return False

# caching is important here to not lose track of the component's reference when populating the page's input fields
@st.cache_resource
def component_creator():
    return StreamlitGraphWidget.from_graph(
        graph = florentine_families_graph(),
        # color the Medici marriage line
        node_color_mapping = lambda node: "#FF5722" if node["properties"]["label"] in medici_line else "#BDBDBD",
        # increase node sizes of Medici marriage line
        node_size_mapping = lambda node: (85, 85) if node["properties"]["label"] in medici_line else (55, 55),
        # highlight edges between Medici marriage line nodes
        edge_styles_mapping = lambda edge: EdgeStyle(
            color="#FF0000" if is_in_medici_line(edge["start"]) and is_in_medici_line(edge["end"]) else "#BDBDBD",
            thickness=6 if is_in_medici_line(edge["start"]) and is_in_medici_line(edge["end"]) else 1
        )
    )

graph = component_creator()

# get the selected nodes and edges from the component with sync_selection=True
selected_nodes, selected_edges = graph.show(sync_selection=True, graph_layout=Layout.HIERARCHIC)
st.write("Selected Edges: ", ", ".join(str(edge["id"]) for edge in selected_edges))
st.write("Selected Nodes: ", ", ".join(str(node["properties"]["label"]) for node in selected_nodes))

st.markdown("---")
st.title("Another component")

# get the selected nodes and edges from the component with sync_selection=True
selected_nodes, selected_edges = graph.show(sync_selection=True, graph_layout=Layout.CIRCULAR, key="2nd component")
st.write("Selected Edges: ", ", ".join(str(edge["id"]) for edge in selected_edges))
st.write("Selected Nodes: ", ", ".join(str(node["properties"]["label"]) for node in selected_nodes))