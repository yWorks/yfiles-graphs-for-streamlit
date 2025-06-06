<p align="center">
    <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/yfiles-graphs-for-streamlit.svg" alt='yFiles Graphs for Streamlit logo'  width="400px" style='max-width: 400px'>
</p>

**Streamlit component for displaying and interacting with graph data powered by [yFiles for HTML](https://www.yfiles.com/the-yfiles-sdk/web/yfiles-for-html?utm_campaign=yfiles4streamlit&utm_source=github&utm_medium=readme).**  
This component enables you to display and interact with graph data directly within your Streamlit apps. It supports full customization of nodes, edges and automatic layouts—making it suitable for a variety of graph-based use cases.

---

## Installation

```bash
pip install yiles-graphs-for-streamlit
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


The Widget is updating selected nodes and edges, such that they can be used in your python script.
They're accessible through `widget.selected_nodes` and `widget.selected_edges`, where widget is just a placeholder for your
created component name.

## Dynamic Property Mappings

Properties can be customized per node/edge in two ways:
1. Directly in the `nodes` or `edges` list.
2. Through dynamic mapping functions.

changeable node arguments:
- `label`
- `color`
    - The default is `#15afac`
- `heat`
- `size`
    - The default is `55,55`
- `type`
- `scale_factor`
    - The default is `1`
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
    - The default is `#15afac`
- `heat` (edges and nodes share a heat mapping)
- `thickness_factor`
    - The default is `1`
- `properties`
- `directed`
    - The default is the given argument when instantiating the Streamlit Widget
- `styles`


Nodes and edges can be modified. E.g. color, size etc.
Node: Each node should have the keys id: int and properties: typing.Dict.

    {'id': ..., 'properties': {'label': ..., ...}}

Edge: Each edge has the keys id: int, start: int, end: int and properties: typing.Dict.

    {id: int, start: int, end: int and properties: typing.Dict.}

### Change node and edges through mapping functions:

To dynamically modify edge properties, use `set_edge_[property]_mapping(...)`.  
All mappings are described in detail down below.

For node properties, use `set_node_[property]_mapping(...)`.

To control the heat values specifically, use `set_heat_mapping(...)`.

Each mapping function receives a node or edge as input and should return the appropriate value for that property.


## Basic Example

```python

import streamlit as st
from Graph_Component import StreamlitGraphWidget

value = StreamlitGraphWidget(
nodes=nodes,
edges=edges,
directed=True,
graph_layout='radial'
)
```

### Feature Highlights

<table>
    <tr>
        <td><a href="https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/main/examples/mapping-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/refs/heads/main/images/mapping.png" title="Mapping visualization" alt="Mapping visualization"></a>
        <td><a href="https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/main/examples/streamlit-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/refs/heads/main/images/introduction.png" title="Heat visualization" alt="Heat data visualization"></a>
    </tr>
    <tr>
        <td><a href="https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/main/examples/little-alchemy-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/refs/heads/main/images/little-alchemy.png" title="Interactive item visualization" alt="Interactive item visualization"></a>
        <td><a href="https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/main/examples/geodata-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/refs/heads/main/images/map.png" title="Geodata visualization" alt="-Geodata visualization"></a>
    </tr>
</table>


## Mappings

#### Label Mappings
- `set_node_label_mapping(mapping: Callable[[node], str | Dict]) -> None`
- `set_edge_label_mapping(mapping: Callable[[edge], str | Dict]) -> None`

#### Property Mappings
- `set_node_property_mapping(mapping: Callable[[node], Dict]) -> None`
- `set_edge_property_mapping(mapping: Callable[[edge], Dict]) -> None`

#### Color Mappings
For the color mappings, all CSS color values are accepted:
- `set_node_color_mapping(mapping: Callable[[node], str]) -> None`
- `set_edge_color_mapping(mapping: Callable[[edge], str]) -> None`

#### Styles Mappings
- `set_node_styles_mapping(mapping: Callable[[node], Dict]) -> None`
    - Possible node stylings:
        - `color`: CSS color value
        - `image`: URL or data URL of the image
        - `shape`: One of `'ellipse'`, `'hexagon'`, `'hexagon2'`, `'octagon'`, `'pill'`, `'rectangle'`, `'round-rectangle'`, `'triangle'`
- `set_edge_styles_mapping(mapping: Callable[[edge], Dict]) -> None`
    - Possible edge stylings:
        - `color`: CSS color value
        - `directed`: `Bool`
        - `thickness`: `float`
        - `dashStyle`: `"solid"`, `"dash"`, `"dot"`, `"dash-dot"`, `"dash-dot-dot"`, `"5 10"` or `"5, 10"`

#### Geometry/Appearance Mappings
- `set_node_scale_factor_mapping(mapping: Callable[[node], float]) -> None`
- `set_node_size_mapping(mapping: Callable[[node], Tuple[float, float]]) -> None`
    - Returns: `(width, height)`
- `set_node_layout_mapping(mapping: Callable[[node], Tuple[float, float, float, float]]) -> None`
    - Returns: `(x, y, width, height)`
- `set_node_position_mapping(mapping: Callable[[node], Tuple[float, float]]) -> None`
    - Returns: `(x, y)`
- `set_node_coordinate_mapping(mapping: Callable[[node], Tuple[float, float]]) -> None`
    - Returns: `(latitude, longitude)`

#### Hierarchy/Structure Mappings
- `set_node_type_mapping(mapping: Callable[[node], str]) -> None`
- `set_node_parent_mapping(mapping: Callable[[node], str | int | float]) -> None`
    - Uses existing IDs to convert nodes into group nodes. Does not create new nodes.
- `set_node_parent_group_mapping(mapping: Callable[[node], str | int | float]) -> None`
    - Creates new group nodes from returned group identifiers.

#### Edge-Specific Mappings
- `set_edge_thickness_factor_mapping(mapping: Callable[[edge], float]) -> None`
- `set_directed_mapping(mapping: Callable[[edge], bool]) -> None`

#### Utility/Visual Analytics
- `set_heat_mapping(mapping: Callable[[element], float]) -> None`
    - Returns a value between `0` and `1`



