<p align="center">
    <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/yfiles-graphs-for-streamlit.svg" alt='yFiles Graphs for Streamlit logo'  width="400px" style='max-width: 400px'>
</p>

[![PyPI - Version](https://img.shields.io/pypi/v/yfiles-graphs-for-streamlit?label=pypi%20package&color=%234c1)](https://pypi.org/project/yfiles-graphs-for-streamlit/)

**Streamlit component for displaying and interacting with graph data using [yFiles - the Graph Visualization SDK](https://www.yfiles.com/the-yfiles-sdk).**
This component allows you to display and interact with graph data directly within your Streamlit apps. It supports full customization of nodes, edges, layouts, and behaviors, making it suitable for a wide range of graph-based use cases.

---

## Installation

The component is available in the Python Package Index.

```bash
pip install yfiles_graphs_for_streamlit
````

## Usage

See also [basic-example.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/basic-example.py).

```python

import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget

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

StreamlitGraphWidget(nodes, edges).show()
```

## Examples

You can find more examples in [/examples](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples).

## Providing Data

The nodes / edges lists are required to be lists of `dict`s. There are only few requirements to the structuring of the provided data:

* `nodes: [Dict]`
  * Each node dict must provide an `id` property
* `edges: [Dict]`
  * Each edge dict must provide an `id`, `start` and `end` property that resolve to the node `id`s to form the graph structure.

Optionally, provide additional properties in a `properties` property.

For example, see [basic-example.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/basic-example.py).

To map custom properties to visual features, see [Data-driven visualization mappings](#data-driven-visualization-mappings).

## Feature Highlights

<table>
    <tr>
        <td><a href="https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/main/examples/data-mapping.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/mapping.png" title="Mapping visualization" alt="Mapping visualization"></a>
        <td><a href="https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/main/examples/basic-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/introduction.png" title="Heat visualization" alt="Heat data visualization"></a>
    </tr>
    <tr>
        <td><a href="https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/main/examples/little-alchemy.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/little-alchemy.png" title="Interactive item visualization" alt="Interactive item visualization"></a>
        <td><a href="https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/main/examples/geodata-example.py"><img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/map.png" title="Geodata visualization" alt="-Geodata visualization"></a>
    </tr>
</table>

## Constructor Parameters

The default constructor consumes structured node and edge lists, see [Providing Data](#providing-data) for structural requirements.

The component also provides a named constructor `from_graph(g)` to import from other graph formats. The graph import supports
`neo4j`, `graph_tool`, `networkx`, `pygraphviz` and `pandas` dataframes. For details on the different graph importers, 
see [Graph Importers](https://yworks.github.io/yfiles-jupyter-graphs/03_graph_importers).

Example usage:
```python
from yfiles_graphs_for_streamlit import StreamlitGraphWidget
from networkx import erdos_renyi_graph
graph = StreamlitGraphWidget.from_graph(erdos_renyi_graph(10, 0.3, 2))
# render the graph
graph.show()
```

## Rendering the Component

Call `show()` to render the component in a streamlit file. There are optional arguments with which the embedding can be adjusted:

| Argument         | Type   | Description                                                                                                                                                                                                                                                      | Default                                     |
|------------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| `directed`       | `bool` | Whether the edges should show a direction indicator.                                                                                                                                                                                                             | `True`                                      |
| `graph_layout`   | `str`  | Can be used to specify a general default automatic layout. <br/>Available algorithms are: `'circular'`, `'hierarchic'`, `'organic'`, `'interactive_organic'`, `'orthogonal'`, `'radial'`, `'tree'`, `'map'`, `'orthogonal_edge_router'`, `'organic_edge_router'` | `'organic'`                                 |
| `sync_selection` | `bool` | Whether the component returns the lists of interactively selected nodes and edges. Enabling this may require caching the component to avoid excessive rerendering.                                                                                                      | `False`                                     |
| `sidebar`        | `dict` | Sidebar options: `{enabled, start_with}`. `start_with` may be one of `'Neighborhood'`, `'Data'`, `'Search'`, `'About'`                                                                                                                                           | `{'enabled': False}`                        |
| `neighborhood`   | `dict` | `{max_distance, selected_nodes}` to filter neighbors.                                                                                                                                                                                                            | `{'max_distance': 1, 'selected_nodes': []}` |
| `overview`       | `bool` | Whether the overview is expanded                                                                                                                                                                                                                                 | `True`                                      |
| `highlight`      | `list` | Nodes/edges to highlight.                                                                                                                                                                                                                                        | `[]`                                        |
| `key`            | `str`  | Streamlit's optional unique key for multiple component instances.                                                                                                                                                                                                | `None`                                      |

The return value of `show()` is a reference to the interactively selected node- or edge-dicts iff `sync_selection` is set to `True`. 
For example, see [selection.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/selection.py).

## Data-driven Visualization Mappings

You can adjust the graph visualization on an item basis by providing the following mapping functions.
Each mapping is passed the original data object of your original node / edge data, and you need to return
a mapping specific dict or value to that is reflected in the graph visualization.

### Property Mappings
Specify what data should be put on the items and therefore be considered by the other data mappings
* `set_node_property_mapping(mapping: Callable[[node], Dict]) -> None`
* `set_edge_property_mapping(mapping: Callable[[edge], Dict]) -> None`

By default, the origin dict for each item is returned.

### Label Mappings
Specify the visualized text on each item.
* `set_node_label_mapping(mapping: Callable[[node], str | Dict]) -> None`
* `set_edge_label_mapping(mapping: Callable[[edge], str | Dict]) -> None`

Returning a string will first be resolved against the `properties` of the item's dict and if there is no such property key the value is used as-is. Alternatively, return a dict with the following properties to have full control over the item's text:
* `text: string`: The text that is added to the item.
* `fontSize: number`: The text size.
* `fontWeight: 'bold' | 'bolder' | 'lighter' | 'normal'`: The font thickness.
* `color: string`: The text color.
* `backgroundColor: string`: A color string that is used as the label's background.
* `position: 'center' | 'north' | 'east' | 'south' | 'west'`: The label position at the node.
* `maximumWidth: number`: The maximum width of the label. By default, the label is clipped at the given size, or wrapped when `wrapping` is set.
* `maximumHeight: number`: The maximum height of the label. Clips the label at the given height. May be combined with `wrapping`.
* `wrapping: 'character' | 'character_ellipsis' | 'none' | 'word' | 'word_ellipsis'`: Text wrapping for the label. Must be set in combination with `maximumWidth`.
* `textAlignment: 'center' | 'left' | 'right'`: The horizontal text alignment when `wrapping` is enabled.

### Color Mappings
Specify the color of each item.
* `set_node_color_mapping(mapping: Callable[[node], str]) -> None`
* `set_edge_color_mapping(mapping: Callable[[edge], str]) -> None`

Return any CSS color value (e.g. a color constant, a hex value, an rgb string, etc.).

### Item Visualization Mappings
Specify the visualization properties of nodes and edges.
* `set_node_styles_mapping(mapping: Callable[[node], Dict]) -> None`
  * Available node properties:
    * `color`: CSS color value
    * `image`: URL or data URL of the image
    * `shape`: One of `'ellipse'`, `'hexagon'`, `'hexagon2'`, `'octagon'`, `'pill'`, `'rectangle'`, `'round-rectangle'`, `'triangle'`
* `set_edge_styles_mapping(mapping: Callable[[edge], Dict]) -> None`
  * Available edge properties:
    * `color`: `str` (a CSS color value)
    * `directed`: `Bool`
    * `thickness`: `float`
    * `dashStyle`: `'solid'`, `'dash'`, `'dot'`, `'dash-dot'`, `'dash-dot-dot'`, `'5 10'` or `'5, 10'`
* `set_edge_thickness_factor_mapping(mapping: Callable[[edge], float]) -> None`
  * Controls the thickness of the edges with a factor that is multiplied to its base size.
* `set_directed_mapping(mapping: Callable[[edge], bool]) -> None`
  * Allows specifying which edge should be visualized with direction (indicated by an arrow).

### Geometry Mappings
Specify the location and/or size of nodes. Note that the location of an item is overwritten from an automatic layout,
unless the `no_layout` option is used.
* `set_node_scale_factor_mapping(mapping: Callable[[node], float]) -> None`
  * Controls the node size with a factor that is multiplied to its base size.
* `set_node_size_mapping(mapping: Callable[[node], Tuple[float, float]]) -> None`
  * Controls the node size by width and height by returning a tuple `(width, height)`.
* `set_node_position_mapping(mapping: Callable[[node], Tuple[float, float]]) -> None`
  * Controls the position of the node by returning a tuple: `(x, y)`.
* `set_node_layout_mapping(mapping: Callable[[node], Tuple[float, float, float, float]]) -> None`
  * Controls the bounding box of the nodes (position and size) by returning a 4-tuple: `(x, y, width, height)`.

### Geospatial Mapping
Specify a geo-coordinate for the nodes that is used by the geospatial layout option.
* `set_node_coordinate_mapping(mapping: Callable[[node], Tuple[float, float]]) -> None`
  * The mapping is supposed to return a tuple of `(latitude, longitude)`.

### Hierarchy Mappings
Specify which nodes should be grouped together.
* `set_node_parent_mapping(mapping: Callable[[node], str | int | float]) -> None`
  * This mapping does not create new group nodes and just resolves the mapped id against the given dataset.
    It should be used when the group nodes are already **part of** the given dataset.
* `set_node_parent_group_mapping(mapping: Callable[[node], str | int | float | Dict]) -> None`
  * This mapping always creates new node objects based on the given mapping.
    It should be used when the group nodes are **not part of** the given dataset.
    When returning a dict, it is required to have a "label" property that is used as text. Any other property is added to its "properties" which are considered when executing other mappings.

### Automatic Layout Mappings
Some mappings affect specific automatic layouts
* `set_node_type_mapping(mapping: Callable[[node], str]) -> None`
  * Assign a specific "type" string to each item. This affects most of the automatic layouts such that same types are placed adjacent to each other, if possible.
* `set_node_cell_mapping(mapping: Callable[[node], Tuple[float, float]]) -> None`
  * Assign a cell tuple `(row, column)` to each node. This information is considered by the hierarchical layout and helps to fine-tune the result, for example, to highlight specific structures of the graph or to convey critical information. 

### Heat Mapping
Numeric values on nodes and edges may be visualized as a heatmap overlay on the graph visualization.
* `set_heat_mapping(mapping: Callable[[element], float]) -> None`
  * The returned heat needs to be normalized in-between `0` and `1`.

## Code of Conduct
This project and everyone participating in it is governed by the [Code of Conduct](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to [contact@yworks.com](mailto:contact@yworks.com).

## Feedback
This component is by no means perfect.
If you find something is not working as expected we are glad to receive an issue report from you.
Please make sure to [search for existing issues](https://github.com/yWorks/yfiles-graphs-for-streamlit/search?q=is%3Aissue+repo%3AyWorks%2Fyfiles-graphs-for-streamlit&type=issues) first
and check if the issue is not an unsupported feature or known issue.
If you did not find anything related, report a new issue with necessary information.
Please also provide a clear and descriptive title and stick to the issue templates.
See [issues](https://github.com/yWorks/yfiles-graphs-for-streamlit/issues).

## Dependencies
The following dependencies are bundled with the component (see also [THIRD-PARTY-NOTICES.json](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/THIRD-PARTY-NOTICES.json)).
- [streamlit-component-lib](https://www.npmjs.com/package/streamlit-component-lib)

## Third-Party Libraries Used at Runtime
Additionally, the following libraries are used at runtime of the component (see also [THIRD-PARTY-NOTICES-RUNTIME.json](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/THIRD-PARTY-NOTICES-RUNTIME.json)).
- [@ctrl/tinycolor](https://github.com/scttcper/tinycolor)
- [@mdi/js](https://github.com/Templarian/MaterialDesign-JS)
- [@sentry/browser](https://www.npmjs.com/package/@sentry/browser)
- [leaflet](https://leafletjs.com/)
- [Matomo JS](https://github.com/matomo-org/matomo/tree/5.4.0/js)
- [Vue](https://vuejs.org/)
- [vue-json-viewer](https://github.com/chenfengjw163/vue-json-viewer)

## License
See [LICENSE](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/main/LICENSE.md) file.
