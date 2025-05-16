import streamlit as st
from yfiles_graphs_for_streamlit import GraphComponent
from geopy.geocoders import Nominatim
import time
# This example might take a while to compile due to geopy

city_names = [
    "Tokyo", "Shanghai", "Moscow", "Berlin", "Paris",
    "Madrid", "Rome", "Stockholm", "Johannesburg",
    "London", "São Paulo", "Mumbai", "Seoul", "Istanbul",
    "Cairo", "Lagos", "Sydney", "Mexico City", "Jakarta"
]

geolocator = Nominatim(user_agent="city-node-generator")
nodes = []

for city in city_names:
    location = geolocator.geocode(city)
    if location:
        node = {
            "id": city,
            "label": city,
            "coordinates":
                [location.latitude,
                location.longitude],
            'properties': {"label": city}
        }
        nodes.append(node)
        time.sleep(5)

component = GraphComponent()
component.set_node_color_mapping(lambda node: '#e1c4ff')
component.set_node_styles_mapping(lambda node: {'image':  'https://cdn-icons-png.flaticon.com/512/252/252025.png'})
edges = []

st.set_page_config(
    page_title="YWorks Streamlit Component",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("---")

#container = st.container()
st.title("Geodata")
component(nodes, edges, False, graph_layout='map')

st.markdown("---")
