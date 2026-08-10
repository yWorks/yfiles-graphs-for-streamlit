import streamlit as st
import json
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout, NodeStyle, NodeShape, LabelStyle, FontWeight, EdgeStyle, DashStyle
import pandas as pd
import os

st.set_page_config(page_title="BPMN Process Visualization", layout="wide")

@st.cache_data
def load_bpmn_data():
    path = os.path.join(os.path.dirname(__file__), "resources", "bpmn-data.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data

data = load_bpmn_data()

st.title(data.get("processName", "BPMN Process"))
st.markdown(data.get("description", ""))

# --- Preprocessing ---

# 1. Transform edges: from/to -> start/end, and add IDs
processed_edges = []
for i, e in enumerate(data.get("edges", [])):
    edge = e.copy()
    edge["id"] = f"edge_{i}"
    edge["start"] = e["from"]
    edge["end"] = e["to"]
    processed_edges.append(edge)

# 2. Create a unified nodes list including Pools, Lanes, and Subprocesses as group nodes
all_nodes = []
subprocesses = sorted(list(set(n.get("subprocess") for n in data.get("nodes", []) if n.get("subprocess"))))

# Add Pools as groups
for pool in data.get("pools", []):
    all_nodes.append({
        "id": pool["id"],
        "label": pool["name"],
        "type": "Pool",
        "is_group": True,
        "properties": {"type": "Pool"}
    })
    # Add Lanes as groups
    for lane in pool.get("lanes", []):
        all_nodes.append({
            "id": lane["id"],
            "label": lane["name"],
            "type": "Lane",
            "parentId": pool["id"],
            "is_group": True,
            "properties": {"type": "Lane"}
        })

# Add Subprocesses as groups
for sub in subprocesses:
    # Find which pool/lane this subprocess belongs to
    sample_nodes = [n for n in data.get("nodes", []) if n.get("subprocess") == sub]
    if sample_nodes:
        parent_id = sample_nodes[0].get("lane") or sample_nodes[0].get("pool")
        all_nodes.append({
            "id": f"sub_{sub}",
            "label": f"Subprocess: {sub}",
            "type": "Subprocess",
            "parentId": parent_id,
            "is_group": True,
            "properties": {"type": "Subprocess"}
        })

# Add regular nodes and link them to parents
for node in data.get("nodes", []):
    n = node.copy()
    if node.get("subprocess"):
        n["parentId"] = f"sub_{node['subprocess']}"
    else:
        n["parentId"] = node.get("lane") or node.get("pool")
    
    if "properties" not in n:
        n["properties"] = {}
    n["properties"]["type"] = node.get("type")
    n["is_group"] = False
    all_nodes.append(n)

# --- Styling Mappings ---

def get_node_style(node):
    node_type = node.get("properties", {}).get("type", "Task")
    
    # BPMN-inspired shapes and colors
    if node_type == "Pool":
        return NodeStyle(shape=NodeShape.RECTANGLE, color="#CFD8DC") # Blue Gray
    if node_type == "Lane":
        return NodeStyle(shape=NodeShape.RECTANGLE, color="#ECEFF1")
    if node_type == "Subprocess":
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color="#FAFAFA", dash_style=DashStyle.DOT)
    
    if "StartEvent" in node_type:
        return NodeStyle(shape=NodeShape.ELLIPSE, color="#A5D6A7") # Green
    if "EndEvent" in node_type:
        return NodeStyle(shape=NodeShape.ELLIPSE, color="#EF9A9A") # Red
    if "Gateway" in node_type:
        return NodeStyle(shape=NodeShape.HEXAGON, color="#FFE082") # Amber/Yellow
    if "Task" in node_type:
        return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color="#90CAF9") # Blue
    
    return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color="#EEEEEE")

def get_edge_style(edge):
    edge_type = edge.get("type", "SequenceFlow")
    color = "#444444"
    dash = DashStyle.SOLID
    
    if edge_type == "MessageFlow":
        dash = DashStyle.DASH
        color = "#888888"
    elif edge_type == "ConditionalFlow":
        color = "#1E88E5"
    
    return EdgeStyle(color=color, dash_style=dash, directed=True, thickness=1.5)

def get_edge_label(edge):
    condition = edge.get("condition")
    label = edge.get("label", "")
    if condition:
        return f"[{condition}]"
    return label

# --- Heatmap Logic ---
# Calculate node degrees for heat mapping (complexity indicator)
node_degrees = {}
for e in processed_edges:
    node_degrees[e["start"]] = node_degrees.get(e["start"], 0) + 1
    node_degrees[e["end"]] = node_degrees.get(e["end"], 0) + 1

max_degree = max(node_degrees.values()) if node_degrees else 1

def get_node_heat(node):
    if node.get("is_group"):
        return 0.0
    degree = node_degrees.get(node["id"], 0)
    return degree / max_degree

# --- Sidebar ---
st.sidebar.header("Visualization Settings")
show_labels = st.sidebar.checkbox("Show Edge Labels", value=True)
enable_heat = st.sidebar.checkbox("Enable Heatmap (Connectivity)", value=False)
layout_type = st.sidebar.selectbox("Layout Strategy", 
                                   ["Hierarchical (BPMN standard)", "Orthogonal", "Organic"],
                                   index=0)

layout_map = {
    "Hierarchical (BPMN standard)": Layout.HIERARCHICAL,
    "Orthogonal": Layout.ORTHOGONAL,
    "Organic": Layout.ORGANIC
}

st.sidebar.markdown("---")
st.sidebar.header("BPMN Legend")
st.sidebar.markdown("""
- 🟢 **Start Events**: Ellipse, Green
- 🔴 **End Events**: Ellipse, Red
- 🟡 **Gateways**: Hexagon, Yellow
- 🔵 **Tasks**: Rounded Rect, Blue
- 🏁 **Pools/Lanes**: Rectangles
- 🌫️ **Subprocesses**: Dashed Rounded Rect
- ➡️ **Sequence Flow**: Solid line
- 📧 **Message Flow**: Dashed line
""")

# --- Graph Rendering ---

widget = StreamlitGraphWidget(
    nodes=all_nodes,
    edges=processed_edges,
    node_label_mapping=lambda n: n.get("label", n["id"]),
    node_styles_mapping=get_node_style,
    edge_styles_mapping=get_edge_style,
    edge_label_mapping=get_edge_label if show_labels else lambda e: "",
    node_parent_mapping=lambda n: n.get("parentId"),
    heat_mapping=get_node_heat if enable_heat else None,
)

st.subheader("Interactive BPMN Process Map")
selected = widget.show(
    graph_layout=layout_map[layout_type],
    sync_selection=True,
    sidebar={"enabled": True, "start_with": "Neighborhood"},
    key="bpmn-graph",
    height=1000,
)

# --- Selection Details ---
if selected:
    sel_nodes, sel_edges = selected
    if sel_nodes or sel_edges:
        col1, col2 = st.columns(2)
        with col1:
            if sel_nodes:
                st.write("### Selected Nodes")
                for n in sel_nodes:
                    with st.expander(f"Node: {n.get('label', n['id'])}"):
                        st.json(n)
        with col2:
            if sel_edges:
                st.write("### Selected Edges")
                for e in sel_edges:
                    start_node = next((n["label"] for n in all_nodes if n["id"] == e["start"]), e["start"])
                    end_node = next((n["label"] for n in all_nodes if n["id"] == e["end"]), e["end"])
                    with st.expander(f"Edge: {start_node} → {end_node}"):
                        st.json(e)
else:
    st.info("Select nodes or edges in the graph to see their properties here.")

st.sidebar.markdown("---")
st.sidebar.header("Process Statistics")
st.sidebar.write(f"**Process:** {data.get('processName')}")
st.sidebar.write(f"**Pools:** {len(data.get('pools', []))}")
st.sidebar.write(f"**Total Nodes:** {len(data.get('nodes', []))}")
st.sidebar.write(f"**Sequence Flows:** {len([e for e in data.get('edges', []) if e['type'] == 'SequenceFlow'])}")
st.sidebar.write(f"**Message Flows:** {len([e for e in data.get('edges', []) if e['type'] == 'MessageFlow'])}")
st.sidebar.write(f"**Conditional Flows:** {len([e for e in data.get('edges', []) if e['type'] == 'ConditionalFlow'])}")
