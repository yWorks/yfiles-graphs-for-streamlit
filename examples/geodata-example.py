import streamlit as st
from yfiles_graphs_for_streamlit import StreamlitGraphWidget
import time

city_names = [
        {"name": "Rio de Janeiro", "lat": -22.808903, "lng": -43.243647, "country": "Brazil", "id": "GIG"},
        {"name": "Lima", "lat": -12.021889, "lng": -77.114319, "country": "Peru", "id": "LIM"},
        {"name": "London", "lat": 51.4775, "lng": -0.461389, "country": "UK", "id": "LHR"},
        {"name": "Frankfurt", "lat": 50.033333, "lng": 8.570556, "country": "Germany", "id": "FRA"},
        {"name": "Moscow", "lat": 55.972642, "lng": 37.414589, "country": "Russia", "id": "SVO"},
        {"name": "New Delhi", "lat": 28.5665, "lng": 77.103089, "country": "India", "id": "DEL"},
        {"name": "Shanghai", "lat": 31.143378, "lng": 121.805214, "country": "China", "id": "PVG"},
        {"name": "Hongkong", "lat": 22.308919, "lng": 113.914603, "country": "China", "id": "HKG"},
        {"name": "Tokio", "lat": 35.764722, "lng": 140.386389, "country": "Japan", "id": "NRT"},
        {"name": "Dubai", "lat": 25.252778, "lng": 55.364444, "country": "UAE", "id": "DXB"},
        {"name": "Dakar", "lat": 14.670833, "lng": -17.072778, "country": "Senegal", "id": "DKR"},
        {"name": "Johannesburg", "lat": -26.133694, "lng": 28.242317, "country": "South Africa", "id": "JNB"},
        {"name": "Sydney", "lat": -33.946111, "lng": 151.177222, "country": "Australia", "id": "SYD"},
        {"name": "Nairobi", "lat": -1.319167, "lng": 36.927778, "country": "Kenya", "id": "NBO"},
        {"name": "Atlanta", "lat": 33.639167, "lng": -84.427778, "country": "USA", "id": "ATL"},
        {"name": "New York City", "lat": 40.63975, "lng": -73.778925, "country": "USA", "id": "JFK"},
        {"name": "Cairo", "lat": 30.121944, "lng": 31.405556, "country": "Egypt", "id": "CAI"},
        {"name": "Casablanca", "lat": 33.367467, "lng": -7.589967, "country": "Morocco", "id": "CMN"},
        {"name": "Lagos", "lat": 6.577222, "lng": 3.321111, "country": "Nigeria", "id": "LOS"},
        {"name": "Cape Town", "lat": -33.969444, "lng": 18.597222, "country": "South Africa", "id": "CPT"},
        {"name": "Chengdu", "lat": 30.578333, "lng": 103.946944, "country": "China", "id": "CTU"},
        {"name": "Jakarta", "lat": -6.125567, "lng": 106.655897, "country": "Indonesia", "id": "CGK"},
        {"name": "Teheran", "lat": 35.416111, "lng": 51.152222, "country": "Iran", "id": "IKA"},
        {"name": "Tel Aviv", "lat": 32.011389, "lng": 34.886667, "country": "Israel", "id": "TLV"},
        {"name": "Kuala Lumpur", "lat": 2.745578, "lng": 101.709917, "country": "Malaysia", "id": "KUL"},
        {"name": "Manila", "lat": 14.508647, "lng": 121.019581, "country": "Philippines", "id": "MNL"},
        {"name": "Singapur", "lat": 1.350189, "lng": 103.994433, "country": "Singapore", "id": "SIN"},
        {"name": "Taipeh", "lat": 25.077732, "lng": 121.232822, "country": "Taiwan", "id": "TPE"},
        {"name": "Bangkok", "lat": 13.681108, "lng": 100.747283, "country": "Thailand", "id": "BKK"},
        {"name": "Istanbul", "lat": 40.976922, "lng": 28.814606, "country": "Turkey", "id": "IST"},
        {"name": "Ulaanbaatar", "lat": 47.843056, "lng": 106.766639, "country": "Mongolia", "id": "ULN"},
        {"name": "Melbourne", "lat": -37.673333, "lng": 144.843333, "country": "Australia", "id": "MEL"},
        {"name": "Brisbane", "lat": -27.383333, "lng": 153.118056, "country": "Australia", "id": "BNE"},
        {"name": "Nadi", "lat": -17.755392, "lng": 177.443378, "country": "Fiji", "id": "NAN"},
        {"name": "Auckland", "lat": -37.008056, "lng": 174.791667, "country": "New Zealand", "id": "AKL"},
        {"name": "Paris", "lat": 49.009722, "lng": 2.547778, "country": "France", "id": "CDG"},
        {"name": "Madrid", "lat": 40.4675, "lng": -3.551944, "country": "Spain", "id": "MAD"},
        {"name": "Barcelona", "lat": 41.297078, "lng": 2.078464, "country": "Spain", "id": "BCN"},
        {"name": "Rome", "lat": 41.804444, "lng": 12.250833, "country": "Italy", "id": "FCO"},
        {"name": "Copenhagen", "lat": 55.617917, "lng": 12.655972, "country": "Denmark", "id": "CPH"},
        {"name": "Helsinki", "lat": 60.317222, "lng": 24.963333, "country": "Finland", "id": "HEL"},
        {"name": "Athens", "lat": 37.936358, "lng": 23.944467, "country": "Greece", "id": "ATH"},
        {"name": "Dublin", "lat": 53.421333, "lng": -6.270075, "country": "Ireland", "id": "DUB"},
        {"name": "Reykjavik", "lat": 64.13, "lng": -21.940556, "country": "Iceland", "id": "RKV"},
        {"name": "Oslo", "lat": 60.193917, "lng": 11.100361, "country": "Norway", "id": "OSL"},
        {"name": "Vienna", "lat": 48.110833, "lng": 16.570833, "country": "Austria", "id": "VIE"},
        {"name": "Lisbon", "lat": 38.774167, "lng": -9.134167, "country": "Portugal", "id": "LIS"},
        {"name": "Stockholm", "lat": 59.651944, "lng": 17.918611, "country": "Sweden", "id": "ARN"},
        {"name": "Edinburgh", "lat": 55.95, "lng": -3.3725, "country": "UK", "id": "EDI"},
        {"name": "Chicago", "lat": 41.978603, "lng": -87.904842, "country": "USA", "id": "ORD"},
        {"name": "San Francisco", "lat": 37.618972, "lng": -122.374889, "country": "USA", "id": "SFO"},
        {"name": "Las Vegas", "lat": 36.080056, "lng": -115.15225, "country": "USA", "id": "LAS"},
        {"name": "Toronto", "lat": 43.677222, "lng": -79.630556, "country": "Canada", "id": "YYZ"},
        {"name": "Vancouver", "lat": 49.193889, "lng": -123.184444, "country": "Canada", "id": "YVR"},
        {"name": "Montreal", "lat": 45.47175, "lng": -73.736569, "country": "Canada", "id": "YUL"},
        {"name": "Mexico-City", "lat": 19.436303, "lng": -99.072097, "country": "Mexico", "id": "MEX"},
        {"name": "Guatemala-City", "lat": 14.583272, "lng": -90.527475, "country": "Guatemala", "id": "GUA"},
        {"name": "Buenos Aires", "lat": -34.822222, "lng": -58.535833, "country": "Argentina", "id": "EZE"},
        {"name": "Sao Paulo", "lat": -23.432075, "lng": -46.469511, "country": "Brazil", "id": "GRU"},
        {"name": "Santiago de Chile", "lat": -33.392975, "lng": -70.785803, "country": "Chile", "id": "SCL"},
        {"name": "Brasilia", "lat": -15.871111, "lng": -47.918611, "country": "Brazil", "id": "BSB"},
        {"name": "Bogota", "lat": 4.701594, "lng": -74.146947, "country": "Colombia", "id": "BOG"},
        {"name": "Caracas", "lat": 10.601194, "lng": -66.991222, "country": "Venezuela", "id": "CCS"}
    ]


nodes = []

for city in city_names:
    location = city['lat'],  city['lng']
    if location:
        node = {
            "id": city['id'],
            "label": city['name'],
            "coordinates":
                [location[0],
                location[1]],
            'properties': {"label": city['name']}
        }
        nodes.append(node)

connections_json = [
    {'from': 'LAX','to': 'JFK' },   {'from': 'JFK','to': 'GIG' },    {'from': 'JFK','to': 'LIM' },    {'from': 'JFK','to': 'LHR' },    {'from': 'GIG','to': 'FRA' },    {'from': 'LIM','to': 'GIG' },    {'from': 'FRA','to': 'JFK' },    {'from': 'LHR','to': 'FRA' },    {'from': 'FRA','to': 'SVO' },    {'from': 'FRA','to': 'DXB' },    {'from': 'SVO','to': 'DEL' },
    {'from': 'SVO','to': 'PVG' },    {'from': 'DEL','to': 'HKG' },    {'from': 'PVG','to': 'HKG' },    {'from': 'PVG','to': 'NRT' },    {'from': 'HKG','to': 'SYD' },    {'from': 'NRT','to': 'SYD' },    {'from': 'DXB','to': 'SVO' },    {'from': 'DXB','to': 'DEL' },    {'from': 'DXB','to': 'DKR' },    {'from': 'DXB','to': 'JNB' },    {'from': 'JNB','to': 'LHR' },
    {'from': 'JNB','to': 'DKR' },    {'from': 'SYD','to': 'DXB' },    {'from': 'NBO','to': 'JNB' },    {'from': 'NBO','to': 'DXB' },    {'from': 'ATL','to': 'JFK' },    {'from': 'LAX','to': 'ATL' },    {'from': 'ATL','to': 'LHR' },    {'from': 'ATL','to': 'LIM' },    {'from': 'SCL','to': 'LIM' },    {'from': 'EZE','to': 'SCL' },    {'from': 'SCL','to': 'GRU' },
    {'from': 'GIG','to': 'EZE' },    {'from': 'GIG','to': 'GRU' },    {'from': 'BSB','to': 'GIG' },    {'from': 'SCL','to': 'BSB' },    {'from': 'LIM','to': 'BSB' },    {'from': 'BOG','to': 'BSB' },    {'from': 'CCS','to': 'BSB' },    {'from': 'BOG','to': 'GUA' },    {'from': 'CCS','to': 'MIA' },    {'from': 'GUA','to': 'MIA' },    {'from': 'GUA','to': 'MEX' },
    {'from': 'MEX','to': 'LAX' },    {'from': 'MEX','to': 'LAX' },    {'from': 'LAX','to': 'SFO' },    {'from': 'SFO','to': 'YVR' },    {'from': 'LAX','to': 'LAS' },    {'from': 'LAX','to': 'DFW' },    {'from': 'LAX','to': 'ORD' },    {'from': 'SFO','to': 'LAS' },    {'from': 'DFW','to': 'ATL' },    {'from': 'ATL','to': 'YYZ' },    {'from': 'ORD','to': 'YYZ' },
    {'from': 'YYZ','to': 'YUL' },    {'from': 'YYZ','to': 'JFK' },    {'from': 'YUL','to': 'JFK' },    {'from': 'JNB','to': 'CPT' },    {'from': 'LOS','to': 'DKR' },    {'from': 'NBO','to': 'LOS' },    {'from': 'DKR','to': 'CMN' },    {'from': 'DKR','to': 'CAI' },    {'from': 'NBO','to': 'CAI' },    {'from': 'DXB','to': 'CAI' },    {'from': 'IKA','to': 'DXB' },
    {'from': 'IST','to': 'IKA' },    {'from': 'TLV','to': 'ATH' },    {'from': 'CAI','to': 'TLV' },    {'from': 'ATH','to': 'IST' },    {'from': 'FCO','to': 'ATH' },    {'from': 'LIS','to': 'LHR' },    {'from': 'LIS','to': 'MAD' },    {'from': 'MAD','to': 'BCN' },    {'from': 'CDG','to': 'LHR' },    {'from': 'DUB','to': 'LHR' },    {'from': 'EDI','to': 'LHR' },
    {'from': 'CDG','to': 'BCN' },    {'from': 'BCN','to': 'FCO' },    {'from': 'VIE','to': 'IST' },    {'from': 'VIE','to': 'SVO' },    {'from': 'CMN','to': 'LIS' },    {'from': 'MAD','to': 'CMN' },    {'from': 'FRA','to': 'CPH' },    {'from': 'LHR','to': 'CPH' },    {'from': 'CPH','to': 'OSL' },    {'from': 'CPH','to': 'ARN' },    {'from': 'ARN','to': 'HEL' },
    {'from': 'HEL','to': 'SVO' },    {'from': 'ULN','to': 'PVG' },    {'from': 'CTU','to': 'PVG' },    {'from': 'PVG','to': 'TPE' },    {'from': 'CTU','to': 'HKG' },    {'from': 'TPE','to': 'HKG' },    {'from': 'HKG','to': 'MNL' },    {'from': 'BKK','to': 'HKG' },    {'from': 'SIN','to': 'KUL' },    {'from': 'SIN','to': 'BKK' },    {'from': 'CGK','to': 'SIN' },
    {'from': 'MNL','to': 'SIN' },    {'from': 'SIN','to': 'SYD' },    {'from': 'BNE','to': 'SYD' },    {'from': 'SYD','to': 'MEL' },    {'from': 'NAN','to': 'SYD' },    {'from': 'AKL','to': 'SYD' },    {'from': 'NAN','to': 'AKL' },    {'from': 'RKV','to': 'LHR' },    {'from': 'BCN','to': 'CDG' },    {'from': 'BCN','to': 'FRA' },    {'from': 'FCO','to': 'FRA' },
    {'from': 'BOG','to': 'MEX' },    {'from': 'BOG','to': 'GRU' },    {'from': 'ATL','to': 'MIA' },    {'from': 'FRA','to': 'IST' },    {'from': 'IST','to': 'DEL' },    {'from': 'PVG','to': 'BKK' },    {'from': 'DEL','to': 'BKK' },
  ]


component = StreamlitGraphWidget()
component.set_node_color_mapping(lambda node: '#e1c4ff')
component.set_node_styles_mapping(lambda node: {'image':  'https://cdn-icons-png.flaticon.com/512/252/252025.png'})
component.set_edge_styles_mapping(lambda edge: {'dashStyle': 'dash', 'color': 'black'})
edges = [
        {"start": connection['from'], "end": connection['to'], "label": "", "properties": {}, "directed": False}
        for connection in connections_json
    ]

st.set_page_config(
    page_title="YWorks Streamlit Component",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("---")

st.title("Geodata")
component(nodes, edges, False, graph_layout='map')

st.markdown("---")
