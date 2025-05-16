<p align="center">
    <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/yfiles-graphs-for-streamlit.svg" alt='yFiles Graphs for Streamlit logo'  width="400px" style='max-width: 400px'>
</p>

**Streamlit component for displaying and interacting with graph data using [yFiles](https://www.yworks.com/products/yfiles).**
This component lets you display and interact with graph data directly in your Streamlit apps. It supports full customization of nodes, edges, layout, and behavior, making it useful for a variety of graph-based use cases.

---

## Installation

```bash
pip install streamlit-yfiles-graph-component
````

## Component Parameters

| Argument       | Type   | Description                                            | Default                                     |
| -------------- | ------ |--------------------------------------------------------| ------------------------------------------- |
| `nodes`        | `list` | List of node dictionaries                              | `[]`                                        |
| `edges`        | `list` | List of edge dictionaries                              | `[]`                                        |
| `directed`     | `bool` | Whether the edges should be displayed as directed      | `False`                                     |
| `graph_layout` | `str`  | Graph layout algorithm (`'organic'`, `'radial'`, etc.) | `'organic'`                                 |
| `sidebar`      | `dict` | Sidebar options: `{enabled, start_with}`               | `{'enabled': True, 'start_with': ''}`       |
| `neighborhood` | `dict` | `{max_distance, selected_nodes}` to filter neighbors   | `{'max_distance': 1, 'selected_nodes': []}` |
| `overview`     | `dict` | Overview options                                       | `{'enabled': True, 'overview_set': True}`   |
| `highlight`    | `list` | Nodes/edges to highlight                               | `[]`                                        |
| `key`          | `str`  | Optional unique key for multiple component instances   | `None`                                      |


## Dynamic Property Mappings

Properties can be customized per node/edge in two ways:
1. Directly in the `nodes` or `edges` list.
2. Through dynamic mapping functions.

changeable node arguments:
- `label`
- `color`
- `heat` 
- `size`
- `type`
- `scale_factor`
- `properties`
- `styles`
- `position`
- `layout`
- `cell`
- `coordinate`
- `parent`
- `heat` (edges and nodes share a heat mapping)

changeable edge arguments: 

- `label`
- `color`
- `heat` (edges and nodes share a heat mapping)
- `thickness_factor`
- `properties`
- `directed`
- `styles`


### 1. Change node and edge

Nodes and edges can be modified. E.g. color, size etc. 
To do so, change the respective field of a node/edge.
Every node is structured like this:


    {'id': ..., 'properties': {'label': ..., ...}, 'color': ..., 'size': (55,55)}
    

Every edge is structured like this:
    

    {'id': ..., 'start': ..., 'end': ..., 'properties': {'label': ..., ...} , 'color': ...}

### 2. Change node and edges through mapping functions:

To dynamically modify edge properties, use `set_edge_[property]_mapping(...)`.  


For node properties, use `set_node_[property]_mapping(...)`.

To control the heat values specifically, use `set_heat_mapping(...)`.

Each mapping function receives a node or edge as input and should return the appropriate value for that property.

For more detailed documentation on available mappings and their behavior, see the [yFiles Jupyter Graphs documentation](https://yworks.github.io/yfiles-jupyter-graphs/).


## Basic Example

```python

import streamlit as st
from Graph_Component import GraphComponent

# Example input data
nodes = [{'id': 'A', 'properties': {'label': 'Node A'}, 'color': 'red', 'size': (50, 50)}]
edges = [{'id': 'e1', 'start': 'A', 'end': 'B', 'properties': {'label': 'connects A to B'}}]

# Render the graph component
value = GraphComponent(
nodes=nodes,
edges=edges,
directed=True,
graph_layout='radial'
)
```

### Feature Highlights

<table>
    <tr>
        <td><a href="https://github.com/yWorks/yfiles-jupyter-graphs-for-streamlit/blob/main/examples/mapping-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-jupyter-graphs-for-streamlit/refs/heads/main/images/mapping.png" title="Mapping visualization" alt="Mapping visualization"></a>
        <td><a href="https://github.com/yWorks/yfiles-jupyter-graphs-for-streamlit/blob/main/examples/streamlit-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-jupyter-graphs-for-streamlit/refs/heads/main/images/introduction.png" title="Heat visualization" alt="Heat data visualization"></a>
    </tr>
    <tr>
        <td><a href="https://github.com/yWorks/yfiles-jupyter-graphs-for-streamlit/blob/main/examples/little-alchemy-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-jupyter-graphs-for-streamlit/refs/heads/main/images/little-alchemy.png" title="Interactive item visualization" alt="Interactive item visualization"></a>
        <td><a href="https://github.com/yWorks/yfiles-jupyter-graphs-for-streamlit/blob/main/examples/geodata-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-jupyter-graphs-for-streamlit/refs/heads/main/images/map.png" title="Geodata visualization" alt="-Geodata visualization"></a>
    </tr>
</table>