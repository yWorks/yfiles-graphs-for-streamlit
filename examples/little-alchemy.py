import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget

# Load little alchemy data
import urllib.request, json

st.set_page_config(page_title="yFiles Graphs for Streamlit", layout="wide")

@st.cache_data
def load_data():
    with urllib.request.urlopen("https://unpkg.com/little-alchemy-2@0.0.1/dist/alchemy.json") as url:
        return json.load(url)

data = load_data()

import itertools

# we'll use a subset of the graph here
num_elements = 50
dataset = dict(itertools.islice(data.items(), num_elements))

parentSet = set()
element_id = None


def custom_images(node):
    return {'image': "https://littlealchemy2.com/static/icons/" + node['id'] + ".svg"}


def custom_size(node):
    if 'prime' in data[str(node['id'])]:
        return 80, 80
    return 55, 55


# This function generates edge labels
def getCombinations(id, target_id):
    result = []
    item = data[target_id]
    for source1, source2 in item['p']:
        if source1 == id:
            result.append(data[source2]['n'])
        if source2 == id:
            result.append(data[source1]['n'])
    return result

def update(element):
    nodes = []
    edges = []
    for key, item in data.items():
        if item['n'] == element:
            nodes.append({"id": key, 'properties': {'label': item['n']}})
            element_id = key
            if 'p' in item:
                for source1, source2 in item['p']:
                    parentSet.add(source1)
                    parentSet.add(source2)
            if 'c' in item:
                for child in item['c']:
                    if child not in parentSet:
                        nodes.append({"id": child, 'properties': {'label': data[child]['n']}})
                        edges.append({"start": key, "end": child, "properties": {
                            'label': '+ ' + str(getCombinations(element_id, child))[1:-1].replace("\'", "")}})
                    else:
                        edges.append({"start": key, "end": child, "properties": {
                            'label': '+ ' + str(getCombinations(element_id, child))[1:-1].replace("\'", "")}})

    return nodes, edges

# Place text input in a narrow column
col1, col2 = st.columns([1, 3])  # 1: narrow, 3: wide

with col1:
    element_name = st.text_input('Enter an element name:', placeholder='e.g. cat')
    edge_color = st.text_input('Enter an edge color:', placeholder='e.g. blue or #0000FF')
    node_size = st.slider("Change the node size:", 0.05, 5.0, 1.0)

if element_name == '':
    element_name = 'butterfly'
nodes, edges = update(element_name)

graph = StreamlitGraphWidget(nodes, edges)
graph.set_node_styles_mapping(custom_images)
graph.set_node_size_mapping(custom_size)
graph.set_edge_color_mapping(lambda: 'gray' if edge_color == '' else edge_color)
graph.set_node_scale_factor_mapping(lambda: node_size)

with col2:
    graph.show(
        graph_layout='hierarchic',
        overview=False,
    )
