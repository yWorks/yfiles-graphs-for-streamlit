import streamlit as st
import json
import os
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout, NodeStyle, NodeShape, EdgeStyle

st.set_page_config(page_title="Pharma Supply Chain Visualization", layout="wide")

@st.cache_data
def load_data():
    path = os.path.join(os.path.dirname(__file__), "resources", "pharma-supply-chain-data.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data

data = load_data()
meta = data.get("meta", {})
groups = data.get("groups", [])
nodes_data = data.get("nodes", [])
edges_data = data.get("edges", [])
products = data.get("products", [])

st.title(meta.get("name", "Pharma Supply Chain"))
st.markdown(meta.get("description", ""))

# Preprocessing
# 1. Transform edges: source/target -> start/end
processed_edges = []
for e in edges_data:
    edge = e.copy()
    edge["start"] = e["source"]
    edge["end"] = e["target"]
    processed_edges.append(edge)

# 2. Merge groups into nodes for hierarchy
# We need to distinguish between groups and leaf nodes for styling
all_nodes = []
for g in groups:
    if g["id"] == "group_global":
        continue
    node = g.copy()
    # Ensure it has a properties dict if we want to use generic mappings
    node["properties"] = {"is_group": True, "label": g["label"], "type": "group"}
    all_nodes.append(node)

for n in nodes_data:
    node = n.copy()
    if "properties" not in node:
        node["properties"] = {}
    node["properties"]["is_group"] = False
    # Link to group hierarchy
    node["parentId"] = node.get("groupId")
    all_nodes.append(node)

all_nodes_dict = {n["id"]: n for n in all_nodes}

# Sidebar filters
st.sidebar.header("Filters & Settings")
regions = sorted(list(set(g["label"] for g in groups if g["level"] == 1)))
selected_region = st.sidebar.multiselect("Filter by Region", regions, default=["Asia", "Europe", "Latin America"])

node_types = sorted(list(set(n["type"] for n in nodes_data)))
selected_types = st.sidebar.multiselect("Filter by Node Type", node_types, default=node_types)

materials = sorted(list(set(e.get("label", "") for e in processed_edges if e.get("label"))))
selected_materials = st.sidebar.multiselect("Filter by Material/Product", materials, default=[])

risk_threshold = st.sidebar.slider("Minimum Risk Score (Nodes)", 0, 100, 0)

# Filtering logic
filtered_node_ids = set()
filtered_edge_ids = set()

# First filter edges by material if selected
if selected_materials:
    for e in processed_edges:
        if e.get("label") in selected_materials:
            filtered_edge_ids.add(e["id"])
            filtered_node_ids.add(e["start"])
            filtered_node_ids.add(e["end"])
else:
    # If no material selected, all edges are candidates
    filtered_edge_ids = set(e["id"] for e in processed_edges)

# Then refine nodes by region, type, risk
final_filtered_node_ids = set()
for nid in filtered_node_ids if selected_materials else [n["id"] for n in nodes_data]:
    n = all_nodes_dict.get(nid)
    if not n or n.get("properties", {}).get("is_group"):
        continue
    
    match_region = not selected_region or n.get("region") in selected_region
    match_type = not selected_types or n.get("type") in selected_types
    match_risk = n.get("properties", {}).get("riskScore", 0) >= risk_threshold
    
    if match_region and match_type and match_risk:
        final_filtered_node_ids.add(n["id"])

# If materials were selected, we only want edges between the remaining nodes
if selected_materials:
    final_filtered_edge_ids = set()
    for eid in filtered_edge_ids:
        e = next(x for x in processed_edges if x["id"] == eid)
        if e["start"] in final_filtered_node_ids and e["end"] in final_filtered_node_ids:
            final_filtered_edge_ids.add(eid)
else:
    # If no materials, filter edges by the final nodes
    final_filtered_edge_ids = set()
    for e in processed_edges:
        if e["start"] in final_filtered_node_ids and e["end"] in final_filtered_node_ids:
            final_filtered_edge_ids.add(e["id"])

# Add parents of filtered nodes to keep hierarchy intact
# Add parents of filtered nodes to keep hierarchy intact
def add_parents(node_id, all_nodes_dict, target_set):
    node = all_nodes_dict.get(node_id)
    if not node:
        return
    parent_id = node.get("parentId")
    if parent_id and parent_id not in target_set:
        target_set.add(parent_id)
        add_parents(parent_id, all_nodes_dict, target_set)

final_node_ids = set(final_filtered_node_ids)
for nid in final_filtered_node_ids:
    add_parents(nid, all_nodes_dict, final_node_ids)

display_nodes = [n for n in all_nodes if n["id"] in final_node_ids]
display_edges = [e for e in processed_edges if e["id"] in final_filtered_edge_ids]

# Visualization Options
viz_mode = st.sidebar.selectbox("Visualization Mode", ["Supply Chain Flow", "Risk Heatmap"])

# Define Mappings
def get_node_color(node):
    props = node.get("properties", {})
    if props.get("is_group"):
        return "#f0f0f0"
    
    # Default: Color by type
    type_colors = {
        "api_supplier": "#2196f3",
        "excipient_supplier": "#03a9f4",
        "packaging_supplier": "#00bcd4",
        "manufacturer": "#9c27b0",
        "distributor": "#ff9800",
        "pharmacy": "#e91e63"
    }
    return type_colors.get(node.get("type"), "#9e9e9e")

def get_node_shape(node):
    props = node.get("properties", {})
    if props.get("is_group"):
        return NodeShape.ROUND_RECTANGLE
    
    type_shapes = {
        "api_supplier": NodeShape.HEXAGON,
        "manufacturer": NodeShape.RECTANGLE,
        "distributor": NodeShape.PILL,
        "pharmacy": NodeShape.ELLIPSE
    }
    return type_shapes.get(node.get("type"), NodeShape.RECTANGLE)

def get_edge_style(edge):
    props = edge.get("properties", {})
    color = "#999999"
    thickness = 1.0 + (props.get("volumeTonsPerMonth", 0) / 50.0)
    return EdgeStyle(color=color, thickness=thickness, directed=True)

# Graph Widget Setup
widget = StreamlitGraphWidget(
    nodes=display_nodes,
    edges=display_edges,
    node_label_mapping=lambda n: n.get("label", n["id"]),
    node_color_mapping=get_node_color,
    node_styles_mapping=lambda n: NodeStyle(shape=get_node_shape(n)),
    edge_styles_mapping=get_edge_style,
    node_parent_mapping=lambda n: n.get("parentId"),
    edge_label_mapping=lambda e: e.get("label", ""),
    heat_mapping=lambda item: float(item.get("properties", {}).get("riskScore", item.get("properties", {}).get("laneRisk", 0))) / 100.0 if viz_mode == "Risk Heatmap" else 0.0
)

# Layout selection
layout = Layout.HIERARCHICAL

st.subheader(f"Current View: {viz_mode}")
selected = widget.show(
    graph_layout=layout,
    sync_selection=True,
    sidebar={"enabled": True, "start_with": "Neighborhood"},
    key="pharma-graph",
    height=1000
)

# Show details of selection
if selected:
    sel_nodes, sel_edges = selected
    if sel_nodes:
        st.write("### Selected Node Details")
        for n in sel_nodes:
            st.json(n)
    if sel_edges:
        st.write("### Selected Edge Details")
        for e in sel_edges:
            st.json(e)

st.sidebar.markdown("---")
st.sidebar.write(f"Displaying {len(display_nodes)} nodes and {len(display_edges)} edges.")
