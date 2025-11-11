# yFiles Graphs for Streamlit (Python-first coding guide)

The widget is a Streamlit component.

## 1) Installation
```bash
pip install yfiles_graphs_for_streamlit
```

## 2) Minimal working example
```python
import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout

st.set_page_config(page_title="yFiles Graphs for Streamlit", layout="wide")

nodes = [
    {"id": 0, "properties": {"firstName": "Alpha", "label": "Person A"}},
    {"id": 1, "properties": {"firstName": "Bravo", "label": "Person B"}},
    {"id": 2, "properties": {"firstName": "Charlie", "label": "Person C", "has_hat": False}},
    {"id": 3, "properties": {"firstName": "Delta", "label": "Person D", "likes_pizza": True}}
]
edges = [
    {"id": 0, "start": 0, "end": 1, "properties": {"since": "1992", "label": "knows"}},
    {"id": 1, "start": 1, "end": 3, "properties": {"label": "knows", "since": "1992"}},
    {"id": 2, "start": 2, "end": 3, "properties": {"label": "knows", "since": "1992"}},
    {"id": 3, "start": 0, "end": 2, "properties": {"label": "knows", "since": 234}}
]

graph = StreamlitGraphWidget(nodes, edges)

# Return tuple (selected_nodes, selected_edges) only when sync_selection=True
selected_nodes, selected_edges = graph.show()
st.write("Selected Edges:", ", ".join(str(e["id"]) for e in selected_edges))
st.write("Selected Nodes:", ", ".join(str(n["id"]) for n in selected_nodes))

# A second widget on the same page must have a unique key
selected_nodes2, selected_edges2 = graph.show(
    sync_selection=True,
    graph_layout=Layout.HIERARCHIC,
    key="second_widget"
)
st.write("Second widget (edges):", ", ".join(str(e["id"]) for e in selected_edges2))
st.write("Second widget (nodes):", ", ".join(str(n["id"]) for n in selected_nodes2))
```

## 3) Data model you pass in

- **Nodes:** list of dicts. Each node **must** have `id`. Optional `properties` dict for arbitrary data.
- **Edges:** list of dicts. Each edge **must** have `id`, `start`, `end` referencing node `id`s. Optional `properties` dict.

> The library uses your original dicts; ids may be numbers or strings. Properties can be nested.

## 4) Constructors

```python
from yfiles_graphs_for_streamlit import StreamlitGraphWidget

# Provide nodes/edges directly
widget = StreamlitGraphWidget(nodes, edges)

# Import from other graph formats
widget = StreamlitGraphWidget.from_graph(g)   # supports neo4j, graph_tool, networkx, pygraphviz, pandas
```

**NetworkX example**
```python
from yfiles_graphs_for_streamlit import StreamlitGraphWidget
from networkx import erdos_renyi_graph

g = erdos_renyi_graph(10, 0.3, seed=2)
widget = StreamlitGraphWidget.from_graph(g)
widget.show()
```

## 5) Rendering the component

```python
from yfiles_graphs_for_streamlit import Layout

nodes_sel, edges_sel = widget.show(
    directed=True,                              # default True
    graph_layout=Layout.ORGANIC,                # default Layout.ORGANIC
    sync_selection=False,                       # default False
    sidebar={"enabled": False},                 # or {"enabled": True, "start_with": "Neighborhood"|"Data"|"Search"|"About"}
    neighborhood={"max_distance": 1, "selected_nodes": []},
    overview=True,
    highlight=[],
    key=None
)
```

### Return value of `show()`
- `sync_selection=False` → returns `None`.
- `sync_selection=True`  → returns a **tuple** `(selected_nodes, selected_edges)`; each item is a `List[Dict]` from your original data.

> When placing multiple widgets on a page, set a unique `key` for each. With `sync_selection=True`, consider caching your data to avoid excessive re-rendering.

## 6) Data‑driven visualization mappings

Each setter takes a **callable** that receives your original item dict and returns the specified type.

Each of the following mapping function can also be set as property on the widget. However, due to better type hints, keyword arguments are preferred for defining data mappings.

### Property mappings (what downstream mappings “see”)
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_property_mapping=lambda node: node.get("properties", {}),
    edge_property_mapping=lambda edge: edge.get("properties", {}),
)
# By default, the original dict is returned.
```

### Label mappings
```python
from yfiles_graphs_for_streamlit import LabelStyle, FontWeight, LabelPosition, TextWrapping, TextAlignment

widget = StreamlitGraphWidget(
    nodes,
    edges,
    # Option A: specify a string (resolved first against properties, otherwise used verbatim)
    node_label_mapping="label",
    # Option B: set a lambda, return a LabelStyle
    edge_label_mapping=lambda e: LabelStyle(
        text=e["properties"]["label"],
        font_size=12,
        font_weight=FontWeight.BOLD,
        color="#222",
        background_color="#eef",
        position=LabelPosition.NORTH,
        maximum_width=160,
        wrapping=TextWrapping.WORD,
        text_alignment=TextAlignment.CENTER,
    ),
)
```

### Color mappings (CSS color strings)
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_color_mapping=lambda n: "#4CAF50",
    edge_color_mapping=lambda e: "rgb(120,120,120)",
)
```

### Item visualization mappings
```python
from yfiles_graphs_for_streamlit import NodeStyle, EdgeStyle, NodeShape, DashStyle

widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_styles_mapping=lambda n: NodeStyle(
        color="#1976d2",
        image=None,                        # URL or data URL if desired
        shape=NodeShape.ROUND_RECTANGLE,
    ),
    edge_styles_mapping=lambda e: EdgeStyle(
        color="#999",
        directed=True,
        thickness=2.0,
        dash_style=DashStyle.DASH_DOT,     # or a custom pattern string like "5, 10"
    ),
)
```

Additional edge-specific helpers:
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    # Factor multiplied with the edge's base thickness
    edge_thickness_factor_mapping=lambda e: 1.0 + float(e["properties"].get("weight", 0)),
    # Per-edge directed override
    directed_mapping=lambda e: e["properties"].get("label") == "knows",
)
```

### Geometry mappings
> Automatic layout overwrites positions unless you select `Layout.NO_LAYOUT`.
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_scale_factor_mapping=lambda n: 1.0,
    node_size_mapping=lambda n: (80.0, 30.0),                       # (width, height)
    node_position_mapping=lambda n: (100.0, 200.0),                 # (x, y)
    node_layout_mapping=lambda n: (100.0, 200.0, 80.0, 30.0),       # (x, y, width, height)
)
```

### Geospatial mapping
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_coordinate_mapping=lambda n: (52.5200, 13.4050),  # (latitude, longitude)
)
# Use graph_layout=Layout.MAP to position nodes by geo-coordinates.
```

### Hierarchy mappings (grouping)
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    # If group nodes already exist in your dataset, return their ids:
    node_parent_mapping=lambda n: n["properties"].get("group_id"),
    # If group nodes do NOT exist, create them on the fly (returns id-like value):
    node_parent_group_mapping=lambda n: n["properties"].get("dept", "Group A"),
)
```

### Layout‑affecting mappings
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_type_mapping=lambda n: n["properties"].get("type", "default"),
    node_cell_mapping=lambda n: (n["properties"].get("row", 0), n["properties"].get("col", 0)),
)
```

### Heat mapping (normalized 0..1)
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    heat_mapping=lambda el: float(el["properties"].get("score", 0.0)),
)
```

## 7) Recipes

**A. Labels from a property, colors by boolean**
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_label_mapping=lambda n: "label",
    node_color_mapping=lambda n: "#2e7d32" if n["properties"].get("likes_pizza") else "#9e9e9e",
)
```

**B. Thicker, directed edges for “since 1992”**
```python
widget = StreamlitGraphWidget(
    nodes,
    edges,
    edge_thickness_factor_mapping=lambda e: 2.0 if e["properties"].get("since") == "1992" else 1.0,
    directed_mapping=lambda e: True,
)
```

**C. Geospatial view**
```python
from yfiles_graphs_for_streamlit import Layout

widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_coordinate_mapping=lambda n: (n["properties"]["lat"], n["properties"]["lon"]),
)
widget.show(graph_layout=Layout.MAP)
```

**D. Manual positions (no layout)**
```python
from yfiles_graphs_for_streamlit import Layout

widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_layout_mapping=lambda n: (n["properties"]["x"], n["properties"]["y"], 80, 30),
)
widget.show(graph_layout=Layout.NO_LAYOUT)
```

**E. Group nodes by department**
```python
from yfiles_graphs_for_streamlit import Layout

widget = StreamlitGraphWidget(
    nodes,
    edges,
    node_parent_group_mapping=lambda n: n["properties"].get("department", "Unknown"),
)
widget.show(graph_layout=Layout.HIERARCHIC)
```

**F. Read interactive selection (tuple return)**
```python
selected_nodes, selected_edges = widget.show(sync_selection=True)
```

**G. Highlight specific items**
```python
widget.show(highlight=[nodes[0], edges[2]])
```

## 8) Option reference

| Option           | Type     | Description                                                                                           | Default                                     |
|------------------|----------|-------------------------------------------------------------------------------------------------------|---------------------------------------------|
| `directed`       | bool     | Whether edges show direction indicators.                                                              | `True`                                      |
| `graph_layout`   | `Layout` | Automatic layout. See **Enums → Layout**.                                                             | `Layout.ORGANIC`                            |
| `sync_selection` | bool     | If `True`, `show()` returns `(selected_nodes, selected_edges)`.                                       | `False`                                     |
| `sidebar`        | dict     | Sidebar options: `{"enabled": bool, "start_with": "Neighborhood" or "Data" or "Search"  or "About"}`. | `{"enabled": False}`                        |
| `neighborhood`   | dict     | `{"max_distance": int, "selected_nodes": list}` to filter neighbors.                                  | `{"max_distance": 1, "selected_nodes": []}` |
| `overview`       | bool     | Whether the overview is expanded.                                                                     | `True`                                      |
| `highlight`      | list     | Nodes/edges to highlight.                                                                             | `[]`                                        |
| `key`            | str      | Streamlit unique key for multiple instances.                                                          | `None`                                      |

---

## 9) Enums (import from `yfiles_graphs_for_streamlit`)

### `Layout`
- `Layout.CIRCULAR` — Arrange in a single cycle; bundle edge paths.
- `Layout.CIRCULAR_STRAIGHT_LINE` — Cycle with straight-line edges.
- `Layout.HIERARCHIC` — Layered, directional flow.
- `Layout.ORGANIC` — Force-directed natural layout.
- `Layout.INTERACTIVE_ORGANIC` — Organic that adapts while interacting.
- `Layout.ORTHOGONAL` — Grid-like nodes, right-angled edges.
- `Layout.RADIAL` — Central node with concentric rings.
- `Layout.TREE` — Rooted tree layout.
- `Layout.MAP` — Uses `(lat, lon)` coordinates.
- `Layout.ORTHOGONAL_EDGE_ROUTER` — Right-angle routing emphasis.
- `Layout.ORGANIC_EDGE_ROUTER` — Smooth, curved routing.
- `Layout.NO_LAYOUT` — Do not apply automatic layout (use provided positions).

### `NodeShape`
- `ELLIPSE`, `HEXAGON`, `HEXAGON2`, `OCTAGON`, `PILL`, `RECTANGLE`, `ROUND_RECTANGLE`, `TRIANGLE`

### `DashStyle`
- `SOLID`, `DASH`, `DOT`, `DASH_DOT`, `DASH_DOT_DOT`  
  *(Also accepts custom dash patterns as strings like `"5 10"` or `"5, 10"`.)*

### `FontWeight`
- `BOLD`, `BOLDER`, `NORMAL`, `LIGHTER`

### `TextAlignment` *(multiline only)*
- `CENTER`, `LEFT`, `RIGHT`

### `TextWrapping` *(effective if `maximum_width` is set)*
- `CHARACTER`, `CHARACTER_ELLIPSIS`, `WORD`, `WORD_ELLIPSIS`, `NONE`

### `LabelPosition`
- `CENTER`, `NORTH`, `EAST`, `SOUTH`, `WEST`

---

## 10) Notes & best practices
- Each mapping property can also be passed as a keyword argument to the constructor or `from_graph()`. Due to type hints, keyword arguments are preferred for defining data mappings.
- Use **`Layout.NO_LAYOUT`** to respect manual positions from geometry mappings.
- Prefer **Enums** over raw strings to reduce typos and get IDE completion.
- With **multiple widgets**, always set unique `key` values.
- With **`sync_selection=True`**, debounce downstream expensive operations if selections change frequently.
