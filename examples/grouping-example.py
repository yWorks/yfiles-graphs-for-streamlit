import streamlit as st
from yfiles_graphs_for_streamlit import GraphComponent


airports = [
    {"name": "Los Angeles", "iata": "LAX", "lat": 33.942536, "lng": -118.408075, "passengers": 65000000, "country": "USA", "id": "LAX"}, {"name": "Rio de Janeiro", "iata": "GIG", "lat": -22.808903, "lng": -43.243647, "passengers": 5000000, "country": "Brazil", "id": "GIG"}, {"name": "Lima", "iata": "LIM", "lat": -12.021889, "lng": -77.114319, "passengers": 18000000, "country": "Peru", "id": "LIM"}, {"name": "London", "iata": "LHR", "lat": 51.4775, "lng": -0.461389, "passengers": 61000000, "country": "UK", "id": "LHR"},
    {"name": "Frankfurt", "iata": "FRA", "lat": 50.033333, "lng": 8.570556, "passengers": 48000000, "country": "Germany", "id": "FRA"}, {"name": "Moscow", "iata": "SVO", "lat": 55.972642, "lng": 37.414589, "passengers": 49000000, "country": "Russia", "id": "SVO"}, {"name": "New Delhi", "iata": "DEL", "lat": 28.5665, "lng": 77.103089, "passengers": 39000000, "country": "India", "id": "DEL"}, {"name": "Shanghai", "iata": "PVG", "lat": 31.143378, "lng": 121.805214, "passengers": 32000000, "country": "China", "id": "PVG"},
    {"name": "Hongkong", "iata": "HKG", "lat": 22.308919, "lng": 113.914603, "passengers": 1000000, "country": "China", "id": "HKG"}, {"name": "Tokio", "iata": "NRT", "lat": 35.764722, "lng": 140.386389, "passengers": 15000000, "country": "Japan", "id": "NRT"}, {"name": "Dubai", "iata": "DXB", "lat": 25.252778, "lng": 55.364444, "passengers": 29000000, "country": "UAE", "id": "DXB"}, {"name": "Dakar", "iata": "DKR", "lat": 14.670833, "lng": -17.072778, "passengers": 2000000, "country": "Senegal", "id": "DKR"},
    {"name": "Johannesburg", "iata": "JNB", "lat": -26.133694, "lng": 28.242317, "passengers": 9000000, "country": "South Africa", "id": "JNB"}, {"name": "Sydney", "iata": "SYD", "lat": -33.946111, "lng": 151.177222, "passengers": 44000000, "country": "Australia", "id": "SYD"}, {"name": "Nairobi", "iata": "NBO", "lat": -1.319167, "lng": 36.927778, "passengers": 900000, "country": "Kenya", "id": "NBO"}, {"name": "Atlanta", "iata": "ATL", "lat": 33.639167, "lng": -84.427778, "passengers": 93000000, "country": "USA", "id": "ATL"},
    {"name": "New York City", "iata": "JFK", "lat": 40.63975, "lng": -73.778925, "passengers": 55000000, "country": "USA", "id": "JFK"}, {"name": "Cairo", "iata": "CAI", "lat": 30.121944, "lng": 31.405556, "passengers": 14000000, "country": "Egypt", "id": "CAI"}, {"name": "Casablanca", "iata": "CMN", "lat": 33.367467, "lng": -7.589967, "passengers": 7000000, "country": "Morocco", "id": "CMN"}, {"name": "Lagos", "iata": "LOS", "lat": 6.577222, "lng": 3.321111, "passengers": 5000000, "country": "Nigeria", "id": "LOS"},
    {"name": "Cape Town", "iata": "CPT", "lat": -33.969444, "lng": 18.597222, "passengers": 5000000, "country": "South Africa", "id": "CPT"}, {"name": "Chengdu", "iata": "CTU", "lat": 30.578333, "lng": 103.946944, "passengers": 40000000, "country": "China", "id": "CTU"}, {"name": "Jakarta", "iata": "CGK", "lat": -6.125567, "lng": 106.655897, "passengers": 54000000, "country": "Indonesia", "id": "CGK"}, {"name": "Teheran", "iata": "IKA", "lat": 35.416111, "lng": 51.152222, "passengers": 8000000, "country": "Iran", "id": "IKA"},
    {"name": "Tel Aviv", "iata": "TLV", "lat": 32.011389, "lng": 34.886667, "passengers": 20000000, "country": "Israel", "id": "TLV"}, {"name": "Kuala Lumpur", "iata": "KUL", "lat": 2.745578, "lng": 101.709917, "passengers": 25000000, "country": "Malaysia", "id": "KUL"}, {"name": "Manila", "iata": "MNL", "lat": 14.508647, "lng": 121.019581, "passengers": 8000000, "country": "Philippines", "id": "MNL"}, {"name": "Singapur", "iata": "SIN", "lat": 1.350189, "lng": 103.994433, "passengers": 32000000, "country": "Singapore", "id": "SIN"},
    {"name": "Taipeh", "iata": "TPE", "lat": 25.077732, "lng": 121.232822, "passengers": 800000, "country": "Taiwan", "id": "TPE"}, {"name": "Bangkok", "iata": "BKK", "lat": 13.681108, "lng": 100.747283, "passengers": 65000000, "country": "Thailand", "id": "BKK"}, {"name": "Istanbul", "iata": "IST", "lat": 40.976922, "lng": 28.814606, "passengers": 64000000, "country": "Turkey", "id": "IST"}, {"name": "Ulaanbaatar", "iata": "ULN", "lat": 47.843056, "lng": 106.766639, "passengers": 1000000, "country": "Mongolia", "id": "ULN"},
    {"name": "Melbourne", "iata": "MEL", "lat": -37.673333, "lng": 144.843333, "passengers": 12000000, "country": "Australia", "id": "MEL"}, {"name": "Brisbane", "iata": "BNE", "lat": -27.383333, "lng": 153.118056, "passengers": 23000000, "country": "Australia", "id": "BNE"}, {"name": "Nadi", "iata": "NAN", "lat": -17.755392, "lng": 177.443378, "passengers": 2000000, "country": "Fiji", "id": "NAN"}, {"name": "Auckland", "iata": "AKL", "lat": -37.008056, "lng": 174.791667, "passengers": 21000000, "country": "New Zealand", "id": "AKL"},
    {"name": "Paris", "iata": "CDG", "lat": 49.009722, "lng": 2.547778, "passengers": 57000000, "country": "France", "id": "CDG"}, {"name": "Madrid", "iata": "MAD", "lat": 40.4675, "lng": -3.551944, "passengers": 50000000, "country": "Spain", "id": "MAD"}, {"name": "Barcelona", "iata": "BCN", "lat": 41.297078, "lng": 2.078464, "passengers": 41000000, "country": "Spain", "id": "BCN"}, {"name": "Rome", "iata": "FCO", "lat": 41.804444, "lng": 12.250833, "passengers": 29000000, "country": "Italy", "id": "FCO"},
    {"name": "Copenhagen", "iata": "CPH", "lat": 55.617917, "lng": 12.655972, "passengers": 30000000, "country": "Denmark", "id": "CPH"}, {"name": "Helsinki", "iata": "HEL", "lat": 60.317222, "lng": 24.963333, "passengers": 5000000, "country": "Finland", "id": "HEL"}, {"name": "Athens", "iata": "ATH", "lat": 37.936358, "lng": 23.944467, "passengers": 22000000, "country": "Greece", "id": "ATH"}, {"name": "Dublin", "iata": "DUB", "lat": 53.421333, "lng": -6.270075, "passengers": 32000000, "country": "Ireland", "id": "DUB"},
    {"name": "Reykjavik", "iata": "RKV", "lat": 64.13, "lng": -21.940556, "passengers": 400000, "country": "Iceland", "id": "RKV"}, {"name": "Oslo", "iata": "OSL", "lat": 60.193917, "lng": 11.100361, "passengers": 9000000, "country": "Norway", "id": "OSL"}, {"name": "Vienna", "iata": "VIE", "lat": 48.110833, "lng": 16.570833, "passengers": 10000000, "country": "Austria", "id": "VIE"}, {"name": "Lisbon", "iata": "LIS", "lat": 38.774167, "lng": -9.134167, "passengers": 28000000, "country": "Portugal", "id": "LIS"},
    {"name": "Stockholm", "iata": "ARN", "lat": 59.651944, "lng": 17.918611, "passengers": 7000000, "country": "Sweden", "id": "ARN"}, {"name": "Edinburgh", "iata": "EDI", "lat": 55.95, "lng": -3.3725, "passengers": 14000000, "country": "UK", "id": "EDI"}, {"name": "Chicago", "iata": "ORD", "lat": 41.978603, "lng": -87.904842, "passengers": 54000000, "country": "USA", "id": "ORD"}, {"name": "Dallas", "iata": "DFW", "lat": 32.896828, "lng": -97.037997, "passengers": 73000000, "country": "USA", "id": "DFW"},
    {"name": "San Francisco", "iata": "SFO", "lat": 37.618972, "lng": -122.374889, "passengers": 42000000, "country": "USA", "id": "SFO"}, {"name": "Las Vegas", "iata": "LAS", "lat": 36.080056, "lng": -115.15225, "passengers": 52000000, "country": "USA", "id": "LAS"}, {"name": "Miami", "iata": "MIA", "lat": 25.79325, "lng": -80.290556, "passengers": 50000000, "country": "USA", "id": "MIA"}, {"name": "Toronto", "iata": "YYZ", "lat": 43.677222, "lng": -79.630556, "passengers": 12000000, "country": "Canada", "id": "YYZ"},
    {"name": "Vancouver", "iata": "YVR", "lat": 49.193889, "lng": -123.184444, "passengers": 19000000, "country": "Canada", "id": "YVR"}, {"name": "Montreal", "iata": "YUL", "lat": 45.47175, "lng": -73.736569, "passengers": 15000000, "country": "Canada", "id": "YUL"}, {"name": "Mexico-City", "iata": "MEX", "lat": 19.436303, "lng": -99.072097, "passengers": 46000000, "country": "Mexico", "id": "MEX"}, {"name": "Guatemala-City", "iata": "GUA", "lat": 14.583272, "lng": -90.527475, "passengers": 2000000, "country": "Guatemala", "id": "GUA"},
    {"name": "Buenos Aires", "iata": "EZE", "lat": -34.822222, "lng": -58.535833, "passengers": 5000000, "country": "Argentina", "id": "EZE"}, {"name": "Sao Paulo", "iata": "GRU", "lat": -23.432075, "lng": -46.469511, "passengers": 34000000, "country": "Brazil", "id": "GRU"}, {"name": "Santiago de Chile", "iata": "SCL", "lat": -33.392975, "lng": -70.785803, "passengers": 20000000, "country": "Chile", "id": "SCL"}, {"name": "Brasilia", "iata": "BSB", "lat": -15.871111, "lng": -47.918611, "passengers": 13000000, "country": "Brazil", "id": "BSB"},
    {"name": "Bogota", "iata": "BOG", "lat": 4.701594, "lng": -74.146947, "passengers": 36000000, "country": "Colombia", "id": "BOG"}, {"name": "Caracas", "iata": "CCS", "lat": 10.601194, "lng": -66.991222, "passengers": 8000000, "country": "Venezuela", "id": "CCS"}
  ]
connections = [
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

component = GraphComponent()
component.edges = edges = [
    {"start": connection['from'], "end": connection['to'], "label": "", "properties": {}, "directed": False}
    for connection in connections
]

component.nodes = nodes = [
    {"id": airport['iata'], "properties": {"label": airport['name'], 'passengers': airport['passengers'], 'country': airport['country']}, "coordinates": [airport['lat'], airport['lng']]}
    for airport in airports
]

airport_nodes = [
    {"id": airport['iata'], "properties": {"label": airport['name'], 'passengers': airport['passengers'], 'country': airport['country']}, "coordinates": [airport['lat'], airport['lng']]}
    for airport in airports
]

component.node_parent_group_mapping = "country"

component.node_coordinate_mapping = 'coordinates' # also map the geo-coordinate data because they are available in the dataset

component.node_color_mapping = lambda node: '#fe019a' if 'country' in node['properties'] else ' #B57EDC'
st.set_page_config(
    page_title="YWorks Streamlit Component",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("---")

st.title("Nested Graphs")
component(nodes, edges, False)

st.markdown("---")
