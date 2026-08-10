import streamlit as st
import json
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout, NodeStyle, NodeShape, LabelStyle, FontWeight, TextWrapping, TextAlignment
import os

try:
    st.set_page_config(page_title="Organization Chart Visualization", layout="wide")
except:
    pass

@st.cache_data
def load_orgchart_data():
    path = os.path.join(os.path.dirname(__file__), "resources", "organization-chart-data.json")
    with open(path, "r") as f:
        data = json.load(f)
    return data

data = load_orgchart_data()

# Assign colors to departments (node color and nested label text color)
dept_colors = {
    "d-01": {"node": "#FFCDD2", "text": "#4A607A"}, # Executive (Deep Slate)
    "d-02": {"node": "#E1BEE7", "text": "#4D7C9E"}, # Engineering (Steel Blue)
    "d-03": {"node": "#BBDEFB", "text": "#3F9E87"}, # Finance (Teal/Green)
    "d-04": {"node": "#C8E6C9", "text": "#915FB3"}, # Marketing (Plum/Purple)
    "d-05": {"node": "#FFF9C4", "text": "#D49A3B"}, # Operations (Amber/Gold/Bronze)
    "d-06": {"node": "#FFE0B2", "text": "#D9745C"}, # Human Resources (Coral/Terracotta)
}

st.title("Organization Chart")
st.markdown("Interactive visualization of the company structure, reporting lines, and departments.")

# --- Sidebar ---
st.sidebar.header("Visualization Settings")
layout_type = st.sidebar.selectbox("Layout Strategy", 
                                   ["Tree (Org Chart)", "Hierarchical", "Organic", "Radial"],
                                   index=0)

layout_map = {
    "Tree (Org Chart)": Layout.TREE,
    "Hierarchical": Layout.HIERARCHICAL,
    "Organic": Layout.ORGANIC,
    "Radial": Layout.RADIAL
}

grouping_enabled = st.sidebar.checkbox("Group by Department", value=True)
heat_enabled = st.sidebar.checkbox("Highlight Span of Control (Heatmap)", value=False)

st.sidebar.markdown("---")
st.sidebar.header("Legend")

legend_html = ""
for dept in data.get("departments", []):
    dept_id = dept["id"]
    dept_name = dept["name"]
    color_info = dept_colors.get(dept_id, {"node": "#4A4A4A", "text": "#6A6A6A"})
    node_color = color_info["node"]
    text_color = color_info["text"]
    
    legend_html += f"""
<div style="display: flex; align-items: center; margin-bottom: 8px;">
    <div style="width: 18px; height: 18px; background-color: {node_color}; border: 2px solid {text_color}; border-radius: 4px; margin-right: 10px; flex-shrink: 0;"></div>
    <span style="font-size: 14px; font-weight: 500;">{dept_name}</span>
</div>
"""

st.sidebar.markdown(legend_html, unsafe_allow_html=True)

# --- Preprocessing ---

people = data.get("people", [])
departments = data.get("departments", [])
edges_data = data.get("edges", [])

# Create a lookup for departments
dept_lookup = {d["id"]: d for d in departments}

# 1. Transform edges: source/target -> start/end, and add IDs
processed_edges = []
for i, e in enumerate(edges_data):
    edge = e.copy()
    edge["id"] = f"edge_{i}"
    edge["start"] = e["source"]
    edge["end"] = e["target"]
    processed_edges.append(edge)

# 2. Prepare nodes
all_nodes = []

# We can treat departments as groups. 
# There are two ways to do this:
# A. Add department nodes to the dataset and use node_parent_mapping.
# B. Use node_parent_group_mapping to create them dynamically.
# Let's go with A to have more control over department node properties.

if grouping_enabled:
    for dept in departments:
        all_nodes.append({
            "id": dept["id"],
            "label": dept["name"],
            "type": "department",
            "is_group": grouping_enabled,
            "properties": dept
        })

for person in people:
    node = person.copy()
    node["label"] = f"{person['name']}\n{person['role']}"
    if grouping_enabled:
        node["parentId"] = person.get("departmentId")
    node["type"] = "person"
    node["is_group"] = False
    
    # Extract role level for styling
    role = person["role"].lower()
    if "chief" in role or "ceo" in role or "cfo" in role or "cto" in role:
        node["level"] = "Executive"
    elif "vp" in role:
        node["level"] = "VP"
    elif "manager" in role:
        node["level"] = "Manager"
    else:
        node["level"] = "Staff"
        
    all_nodes.append(node)

# --- Styling Mappings ---

def get_node_style(node):
    if node.get("type") == "department":
        return NodeStyle(shape=NodeShape.RECTANGLE, color="#F5F5F5")
    
    dept_id = node.get("departmentId")
    color_info = dept_colors.get(dept_id, {"node": "#4A4A4A", "text": "#6A6A6A"})
    color = color_info["node"]
    
    return NodeStyle(shape=NodeShape.ROUND_RECTANGLE, color=color)

def get_node_label_style(node):
    if node.get("type") == "department":
        return LabelStyle(text=node.get("label", node["id"]), font_weight=FontWeight.BOLD, font_size=16)
    
    dept_id = node.get("departmentId")
    color_info = dept_colors.get(dept_id, {"node": "#4A4A4A", "text": "#6A6A6A"})
    text_color = color_info["text"]
    
    return LabelStyle(
        text=node.get("label", node["id"]),
        font_weight=FontWeight.BOLD,
        font_size=11,
        color=text_color,
        wrapping=TextWrapping.WRAP_WORD,
        maximum_width=180,
        text_alignment=TextAlignment.CENTER
    )

# --- Heatmap Logic (Influence/Span of Control) ---
# Calculate number of direct reports
reports_count = {}
for e in processed_edges:
    reports_count[e["start"]] = reports_count.get(e["start"], 0) + 1

max_reports = max(reports_count.values()) if reports_count else 1

def get_node_heat(node):
    if node.get("type") == "department":
        return 0.0
    count = reports_count.get(node["id"], 0)
    return count / max_reports

# --- Graph Rendering ---

widget = StreamlitGraphWidget(
    nodes=all_nodes,
    edges=processed_edges,
    node_label_mapping=get_node_label_style,
    node_styles_mapping=get_node_style,
    node_size_mapping=lambda n: (200, 70) if n.get("type") == "person" else (250, 100),
    node_parent_mapping="parentId" if grouping_enabled else None,
    heat_mapping=get_node_heat if heat_enabled else None,
)

selected = widget.show(
    graph_layout=layout_map[layout_type],
    sync_selection=True,
    sidebar={"enabled": True, "start_with": "Search"},
    key="org-graph",
    height=1000,
)

# --- Selection Details ---
if selected:
    sel_nodes, sel_edges = selected
    if sel_nodes:
        st.write("### Selection Details")
        for n in sel_nodes:
            if n.get("type") == "person":
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric("Role", n.get("level"))
                with col2:
                    st.write(f"**{n['name']}**")
                    st.write(f"Role: {n['role']}")
                    st.write(f"Email: {n['email']}")
                    st.write(f"Phone: {n['phone']}")
                    dept = dept_lookup.get(n.get("departmentId"))
                    if dept:
                        st.write(f"Department: {dept['name']}")
            else:
                st.write(f"### Department: {n['name']}")
                st.write(f"Address: {n['address']}")
                st.write(f"Phone: {n['phone']}")
    
    if sel_edges:
        st.write("### Reporting Relationship")
        for e in sel_edges:
            boss = next((n["name"] for n in people if n["id"] == e["start"]), e["start"])
            report = next((n["name"] for n in people if n["id"] == e["end"]), e["end"])
            st.write(f"{report} reports to {boss}")
else:
    st.info("Select a person to see their contact details and role information.")

st.sidebar.markdown("---")
st.sidebar.header("Company Stats")
st.sidebar.write(f"**Total Employees:** {len(people)}")
st.sidebar.write(f"**Departments:** {len(departments)}")
