import streamlit as st
import itertools
import urllib.request, json
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout, NodeStyle

st.set_page_config(page_title="yFiles Graphs for Streamlit", layout="wide")

# load little-alchemy data from the web
@st.cache_data
def load_data():
    with urllib.request.urlopen("https://unpkg.com/little-alchemy-2@0.0.1/dist/alchemy.json") as url:
        return json.load(url)
data = load_data()

# this example only uses a subset of the data
dataset = dict(itertools.islice(data.items(), 50))

def create_edge_label(id, target_id):
    """Generate edge labels"""
    result = []
    item = data[target_id]
    for source1, source2 in item["p"]:
        if source1 == id:
            result.append(data[source2]["n"])
        if source2 == id:
            result.append(data[source1]["n"])
    return result

parentSet = set()
def create_graph_data(element):
    """Creates the node and edge dicts that are visualized as graph"""
    result_nodes = []
    result_edges = []

    if element is None:
        # display a subset of the data
        for key, item in dataset.items():
            result_nodes.append({"id": key, "properties": {"label": item["n"]}})
            if "p" in item:
                for source1, source2 in item["p"]:
                    if source1 in dataset and source2 in dataset:
                        if not source1 == source2:
                            result_edges.append(
                                {"start": source1, "end": key, "properties": {"label": ("+ " + data[source2]["n"])}})
                            result_edges.append(
                                {"start": source2, "end": key, "properties": {"label": ("+ " + data[source1]["n"])}})
                        else:
                            result_edges.append(
                                {"start": source1, "end": key, "properties": {"label": ("+ " + data[source2]["n"])}})
    else:
        # display the data for a specific element by looking at the whole dataset
        for key, item in data.items():
            if item["n"] == element:
                result_nodes.append({"id": key, "properties": {"label": item["n"]}})
                element_id = key
                if "p" in item:
                    for source1, source2 in item["p"]:
                        parentSet.add(source1)
                        parentSet.add(source2)
                if "c" in item:
                    for child in item["c"]:
                        if child not in parentSet:
                            result_nodes.append({"id": child, "properties": {"label": data[child]["n"]}})
                            result_edges.append({"start": key, "end": child, "properties": {
                                "label": "+ " + str(create_edge_label(element_id, child))[1:-1].replace("\"", "")}})
                        else:
                            result_edges.append({"start": key, "end": child, "properties": {
                                "label": "+ " + str(create_edge_label(element_id, child))[1:-1].replace("\"", "")}})

    return result_nodes, result_edges

# Place text input in a narrow column
col1, col2 = st.columns([1, 3])  # 1: narrow, 3: wide

# create input elements
with col1:
    element_name = st.text_input("Enter an element name:", placeholder="e.g. cat")
    edge_color = st.text_input("Enter an edge color:", placeholder="e.g. blue or #0000FF")
    node_size = st.slider("Change the node size:", 0.05, 5.0, 1.0)

# create the structured data based on the given element
nodes, edges = create_graph_data(element_name or None)

graph = StreamlitGraphWidget(
    # pass node and edge dicts
    nodes = nodes,
    edges = edges,
    # use icons for node visualization
    node_styles_mapping = lambda node: NodeStyle(image="https://littlealchemy2.com/static/icons/" + node["id"] + ".svg"),
    # "prime"-nodes should be bigger than other nodes
    node_size_mapping = lambda node: (80, 80) if "prime" in data[str(node["id"])] else (55, 55),
    # color edges
    edge_color_mapping = lambda edge: "gray" if edge_color == "" else edge_color,
    # pass the slider's size value as scale mapping
    node_scale_factor_mapping = lambda node: node_size
)

with col2:
    # render the component with a hierarchic layout and collapsed overview overlay
    graph.show(graph_layout=Layout.HIERARCHIC, overview=False)