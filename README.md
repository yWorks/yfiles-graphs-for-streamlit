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

## Feature Highlights

<table>
    <tr>
        <td>
            <b>Automatic graph layouts</b><br>
            <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/layouts.png" title="Automatic graph layouts" alt="Automatic graph layouts">
        </td>
        <td>
            <b>Item neighborhood</b>
            <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/neighborhood.png" title="Item neighborhood" alt="Item neighborhood">
        </td>
    </tr>
    <tr>
        <td>
            <b>Visualize data as heatmap</b>
            <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/mapping.png" title="Visualize data as heatmap" alt="Visualize data as heatmap">
        </td>
        <td>
            <b>Use geospatial data</b>
            <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/map.png" title="Use geospatial data" alt="Use geospatial data">
        </td>
    </tr>
    <tr>
        <td>
            <b>Data-driven visualization</b>
            <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/little-alchemy.png" title="Data-driven visualization" alt="Data-driven visualization">
        </td>
        <td>
            <b>Grouping and Folding</b>
            <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/nesting.png" title="Grouping and Folding" alt="Grouping and Folding">
        </td>
    </tr>
    <tr>
        <td>
            <b>Import graph data</b>
            <img src="https://raw.githubusercontent.com/yWorks/yfiles-graphs-for-streamlit/main/images/import-code.png" title="Import graph data" alt="Import graph data">
        </td>
    </tr>
</table>

## Examples

You can find example implementations in [/examples](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples).

## Providing Data

The nodes / edges lists are required to be lists of `dict`s. There are only few requirements to the structuring of the provided data:

* `nodes: [Dict]`
  * Each node dict must provide an `id` property
* `edges: [Dict]`
  * Each edge dict must provide an `id`, `start` and `end` property that resolve to the node `id`s to form the graph structure.

Optionally, provide additional properties in a `properties` property.

For example, see [basic-example.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/basic-example.py).

To map custom properties to visual features, see [Data-driven visualization mappings](#data-driven-visualization-mappings).

### Importing from other graph packages

Aside from passing structured data, you can also import from other graph formats:

* `from_graph(graph)`
  * `graph` supports
    `neo4j`, `graph_tool`, `networkx`, `pygraphviz` and `pandas` dataframes. For details on the different graph importers,
    see [Graph Importers](https://yworks.github.io/yfiles-jupyter-graphs/03_graph_importers).

Example usage:
```python
from yfiles_graphs_for_streamlit import StreamlitGraphWidget
from networkx import erdos_renyi_graph
# import other graph packages
graph = StreamlitGraphWidget.from_graph(erdos_renyi_graph(10, 0.3, 2))
# create an interactive graph visualization
graph.show()
```

## Constructor

The default constructor consumes structured node and edge lists, see [Providing Data](#providing-data) for structural requirements.

Alternatively, use the `from_graph` constructor to import from other graph formats ([Importing from other graph packages](#importing-from-other-graph-packages)).

## Rendering the Component

Call `show()` to render the component in a streamlit file. There are optional arguments with which the embedding can be adjusted:

| Argument         | Type     | Description                                                                                                                                                        | Default                                     |
|------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------|
| `directed`       | `bool`   | Whether the edges should show a direction indicator.                                                                                                               | `True`                                      |
| `graph_layout`   | `Layout` | Can be used to specify a general default automatic layout. See [Layout](#layout).                                                                                  | `Layout.ORGANIC`                            |
| `sync_selection` | `bool`   | Whether the component returns the lists of interactively selected nodes and edges. Enabling this may require caching the component to avoid excessive rerendering. | `False`                                     |
| `sidebar`        | `dict`   | Sidebar options: `{enabled, start_with}`. `start_with` may be one of `'Neighborhood'`, `'Data'`, `'Search'`, `'About'`                                             | `{'enabled': False}`                        |
| `neighborhood`   | `dict`   | `{max_distance, selected_nodes}` to filter neighbors.                                                                                                              | `{'max_distance': 1, 'selected_nodes': []}` |
| `overview`       | `bool`   | Whether the overview is expanded                                                                                                                                   | `True`                                      |
| `highlight`      | `list`   | Nodes/edges to highlight.                                                                                                                                          | `[]`                                        |
| `key`            | `str`    | Streamlit's optional unique key for multiple component instances.                                                                                                  | `None`                                      |

The return value of `show()` is a tuple of node and edge lists that are interactively selected. The returned lists are only updated when `sync_selection` is set to `True`.
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
* `set_node_label_mapping(mapping: Callable[[node], str | LabelStyle]) -> None`
* `set_edge_label_mapping(mapping: Callable[[edge], str | LabelStyle]) -> None`

Returning a string will first be resolved against the `properties` of the item's dict and if there is no such property key the value is used as-is. Alternatively, return a `LabelStyle` object with the following properties to have full control over the item's text:
* `text: string`: The text that is added to the item.
* `font_size: int`: The text size.
* `font_weight: FontWeight`: The font weight. See [FontWeight](#fontweight).
* `color: string`: The text color.
* `background_color: string`: A color string that is used as the label's background.
* `position: LabelPosition`: Where the label is placed relatively to the node. See [LabelPosition](#labelposition).
* `maximum_width: int`: The maximum width of the label. By default, the label is clipped at the given size, or wrapped when `wrapping` is set.
* `maximum_height: int`: The maximum height of the label. Clips the label at the given height. May be combined with `wrapping`.
* `wrapping: TextWrapping`: Text wrapping for the label. Must be set in combination with `maximum_width`. See [TextWrapping](#textwrapping).
* `text_alignment: TextAlignment`: The horizontal text alignment when `wrapping` is enabled. See [TextAlignment](#textalignment).

For example, see [data-mapping.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/data-mapping.py).

### Color Mappings
Specify the color of each item.
* `set_node_color_mapping(mapping: Callable[[node], str]) -> None`
* `set_edge_color_mapping(mapping: Callable[[edge], str]) -> None`

Return any CSS color value (e.g. a color constant, a hex value, an rgb string, etc.).

For example, see [data-mapping.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/data-mapping.py).

### Item Visualization Mappings
Specify the visualization properties of nodes and edges.
* `set_node_styles_mapping(mapping: Callable[[node], NodeStyle]) -> None`
  * Available node properties on `NodeStyle`:
    * `color`: CSS color value
    * `image`: URL or data URL of the image
    * `shape`: `NodeShape` enum, see [NodeShape](#nodeshape)
* `set_edge_styles_mapping(mapping: Callable[[edge], EdgeStyle]) -> None`
  * Available edge properties on `EdgeStyle`:
    * `color`: `str` (a CSS color value)
    * `directed`: `bool`
    * `thickness`: `float`
    * `dash_style`: `DashStyle` (see [DashStyle](#dashstyle)) or a dashing string like `'5 10'` or `'5, 10'`
* `set_edge_thickness_factor_mapping(mapping: Callable[[edge], float]) -> None`
  * Controls the thickness of the edges with a factor that is multiplied to its base size.
* `set_directed_mapping(mapping: Callable[[edge], bool]) -> None`
  * Allows specifying which edge should be visualized with direction (indicated by an arrow).

For example, see [data-mapping.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/data-mapping.py).

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

For example, see [data-mapping.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/data-mapping.py).

### Geospatial Mapping
Specify a geo-coordinate for the nodes that is used by the geospatial layout option.
* `set_node_coordinate_mapping(mapping: Callable[[node], Tuple[float, float]]) -> None`
  * The mapping is supposed to return a tuple of `(latitude, longitude)`.

For example, see [geodata.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/geodata.py).

### Hierarchy Mappings
Specify which nodes should be grouped together.
* `set_node_parent_mapping(mapping: Callable[[node], str | int | float]) -> None`
  * This mapping does not create new group nodes and just resolves the mapped id against the given dataset.
    It should be used when the group nodes are already **part of** the given dataset.
* `set_node_parent_group_mapping(mapping: Callable[[node], str | int | float]) -> None`
  * This mapping always creates new dicts based on the given mapping.
    It should be used when the group nodes are **not part of** the given dataset.

For example, see [grouping.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/grouping.py).

### Fine-tuning automatic layouts
Some mappings affect specific automatic layouts
* `set_node_type_mapping(mapping: Callable[[node], str]) -> None`
  * Assign a specific "type" string to each item. This affects most of the automatic layouts such that same types are placed adjacent to each other, if possible.
* `set_node_cell_mapping(mapping: Callable[[node], Tuple[float, float]]) -> None`
  * Assign a cell tuple `(row, column)` to each node. This information is considered by the hierarchical layout and helps to fine-tune the result, for example, to highlight specific structures of the graph or to convey critical information. 

### Heat Mapping
Numeric values on nodes and edges may be visualized as a heatmap overlay on the graph visualization.
* `set_heat_mapping(mapping: Callable[[element], float]) -> None`
  * The returned heat needs to be normalized in-between `0` and `1`.

For example, see [geodata.py](https://github.com/yWorks/yfiles-graphs-for-streamlit/blob/master/examples/geodata.py).

## Enums
The enums can be imported from `yfiles_graphs_for_streamlit`.

### `Layout`
| Enum                            | Description                                                                                                |
|---------------------------------|------------------------------------------------------------------------------------------------------------|
| `Layout.CIRCULAR`               | Arranges nodes in singly cycle and bundles edge paths.                                                     |
| `Layout.CIRCULAR_STRAIGHT_LINE` | Arranges nodes in singly cycle and uses straight-line edge paths.                                          |
| `Layout.HIERARCHIC`             | Organizes nodes in hierarchical layers to emphasize directional flow.                                      |
| `Layout.ORGANIC`                | Uses a force-directed algorithm to create a natural, free-form network layout.                             |
| `Layout.INTERACTIVE_ORGANIC`    | Similar to `ORGANIC` but dynamically adjusts the layout as the user interacts with it.                     |
| `Layout.ORTHOGONAL`             | Positions nodes on a grid with right-angled edges for clear, structured diagrams.                          |
| `Layout.RADIAL`                 | Places a central node in the middle and arranges others in rings around it to show hierarchy or influence. |
| `Layout.TREE`                   | Displays nodes in a branching tree structure from a defined root node.                                     |
| `Layout.MAP`                    | Uses user-defined geo-coordinates to place the nodes on a world map                                        |
| `Layout.ORTHOGONAL_EDGE_ROUTER` | Reroutes edges at right angles to minimize overlap and improve readability.                                |
| `Layout.ORGANIC_EDGE_ROUTER`    | Smoothly routes edges around obstacles in a natural, curved manner.                                        |
| `Layout.NO_LAYOUT`              | Leaves node positions unchanged without applying any automatic layout.                                     |

### `NodeShape`
| Enum                        | Description                                                                                                     |
|-----------------------------|-----------------------------------------------------------------------------------------------------------------|
| `NodeShape.ELLIPSE`         | An elliptical shape.                                                                                            |
| `NodeShape.HEXAGON`         | A 6-sided polygon where the top and bottom edges are aligned with the top and bottom edges of the bounding box. |
| `NodeShape.HEXAGON2`        | A 6-sided polygon where the left and right edges are aligned with the left and right edges of the bounding box. |
| `NodeShape.OCTAGON`         | An 8-sided polygon where the edges are aligned with the edges of the bounding box.                              |
| `NodeShape.PILL`            | A stadium shape with the shorter sides rounded.                                                                 |
| `NodeShape.RECTANGLE`       | A rectangular shape.                                                                                            |
| `NodeShape.ROUND_RECTANGLE` | A rectangular shape with rounded corners.                                                                       |
| `NodeShape.TRIANGLE`        | A triangular shape that points to the top.                                                                      |

### `DashStyle`
| Enum                        | Description                           |
|-----------------------------|---------------------------------------|
| `DashStyle.SOLID`           | Solid line style.                     |
| `DashStyle.DASH`            | Dashed line style.                    |
| `DashStyle.DOT`             | Dotted line style.                    |
| `DashStyle.DASH_DOT`        | Single dash and dot line style        |
| `DashStyle.DASH_DOT_DOT`    | A single dash and two dots line style |


### `FontWeight`
| Enum                 | Description |
|----------------------|-------------|
| `FontWeight.BOLD`    | 'bold'      |
| `FontWeight.BOLDER`  | 'bolder'    |
| `FontWeight.NORMAL`  | 'normal'    |
| `FontWeight.LIGHTER` | 'lighter'   |

### `TextAlignment`
Only affects multiline texts.

| Enum                   | Description                    |
|------------------------|--------------------------------|
| `TextAlignment.CENTER` | Center aligned multiline text. |
| `TextAlignment.LEFT`   | Left aligned multiline text.   |
| `TextAlignment.RIGHT`  | right aligned multiline text.  |

### `TextWrapping`
Is only in effect when `maximum_width` is specified on `LabelStyle`.

| Enum                              | Description                                                              |
|-----------------------------------|--------------------------------------------------------------------------|
| `TextWrapping.CHARACTER`          | Character wrapping at `maximum_width`  .                                 |
| `TextWrapping.CHARACTER_ELLIPSIS` | Character wrapping at `maximum_width` with ellipsis at `maximum_height`. |
| `TextWrapping.WORD`               | Word wrapping at `maximum_width`.                                        |
| `TextWrapping.WORD_ELLIPSIS`      | Word wrapping at `maximum_width` with ellipsis at `maximum_height`.      |
| `TextWrapping.NONE`               | The text is not wrapped, nor clipped.                                    |

### `LabelPosition`
| Enum                   | Description                                                |
|------------------------|------------------------------------------------------------|
| `LabelPosition.CENTER` | Places the label in the center of the node (interior).     |
| `LabelPosition.NORTH`  | Places the label above the node (exterior).                |
| `LabelPosition.EAST`   | Places the label on the right side of the node (exterior). |
| `LabelPosition.SOUTH`  | Places the label below the node (exterior).                |
| `LabelPosition.WEST`   | Places the label on the left side of the node (exterior).  |

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