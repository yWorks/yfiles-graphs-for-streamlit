import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout, LabelStyle, FontWeight, EdgeStyle
from networkx import florentine_families_graph

st.set_page_config(
    page_title="yFiles Graphs for Streamlit",
    layout="wide",
)

st.markdown("---")
st.title("Data-driven visualization")

# Medici marriage line
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

graph = StreamlitGraphWidget.from_graph(
    # import NetworkX sample graph
    graph = florentine_families_graph(),
    # color Medici marriage line
    node_color_mapping = lambda node: "#FF5722" if node["properties"]["label"] in medici_line else "#BDBDBD",
    # increase node sizes of Medici marriage line
    node_size_mapping = lambda node: (85, 85) if node["properties"]["label"] in medici_line else (55, 55),
    # apply a heat mapping to the Medici marriage line
    heat_mapping = lambda item: 0.5 if item["properties"]["label"] in medici_line else 0.0,
    # highlight edges between Medici marriage line nodes
    edge_styles_mapping = lambda edge: EdgeStyle(
        color = "#FF0000" if is_in_medici_line(edge["start"]) and is_in_medici_line(edge["end"]) else "#BDBDBD",
        thickness = 6 if is_in_medici_line(edge["start"]) and is_in_medici_line(edge["end"]) else 1
    ),
    # emphasize Medici marriage line node labels
    node_label_mapping = lambda n: LabelStyle(
        text = n["properties"]["label"],
        font_weight = FontWeight.BOLD if n["properties"]["label"] in medici_line else FontWeight.NORMAL,
        font_size = 16 if n["properties"]["label"] in medici_line else 12
    )
)

# render the component
graph.show(graph_layout=Layout.HIERARCHIC)

st.markdown("---")
