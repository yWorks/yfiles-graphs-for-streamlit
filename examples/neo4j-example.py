import streamlit as st
from neo4j import GraphDatabase
from yfiles_graphs_for_streamlit import StreamlitGraphWidget, Layout, Node, Edge

st.set_page_config(page_title="Neo4j Movies Graph", layout="wide")

st.title("Neo4j Movies Database Visualization")
st.write("Visualizing data from the Neo4j movies sample database using yFiles Graphs for Streamlit")

# Neo4j connection details https://github.com/neo4j-graph-examples/recommendations
NEO4J_URI = "neo4j+s://demo.neo4jlabs.com"
NEO4J_USER = "recommendations"
NEO4J_PASSWORD = "recommendations"
NEO4J_DATABASE = "recommendations"

@st.cache_resource
def get_neo4j_driver():
    """Create and cache Neo4j driver connection"""
    return GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def query_neo4j(query, limit=20):
    """Execute a Cypher query and return results"""
    driver = get_neo4j_driver()
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run(query, limit=limit)
        # Return records, not .data() which serializes to dicts
        return list(result)

# Query selector
st.sidebar.header("Query Options")
query_type = st.sidebar.selectbox(
    "Select Query Type",
    ["Movies and Actors", "Movies and Genres", "User Ratings", "Custom Query"]
)

limit = st.sidebar.slider("Limit Results", 5, 50, 20)

# Define queries based on selection
if query_type == "Movies and Actors":
    cypher_query = """
    MATCH (a:Person)-[r:ACTED_IN]->(m:Movie)
    RETURN a, r, m
    LIMIT $limit
    """
elif query_type == "Movies and Genres":
    cypher_query = """
    MATCH (m:Movie)-[r:IN_GENRE]->(g:Genre)
    RETURN m, r, g
    LIMIT $limit
    """
elif query_type == "User Ratings":
    cypher_query = """
    MATCH (u:User)-[r:RATED]->(m:Movie)
    RETURN u, r, m
    LIMIT $limit
    """
else:
    custom_query = st.sidebar.text_area(
        "Enter Custom Cypher Query",
        "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 10"
    )
    cypher_query = custom_query

try:
    # Execute query
    with st.spinner("Fetching data from Neo4j..."):
        results = query_neo4j(cypher_query, limit)
    
    if not results:
        st.warning("No results returned from the query.")
    else:
        st.success(f"Retrieved {len(results)} records")
        
        # Convert Neo4j results to nodes and edges
        nodes = {}
        edges = []
        edge_id = 0
        
        from neo4j.graph import Node as Neo4jNode, Relationship
        
        for record in results:
            # Access values from the record
            for key in record.keys():
                value = record[key]
                # Check if it's a Neo4j Node
                if isinstance(value, Neo4jNode):
                    node_id = value.element_id
                    if node_id not in nodes:
                        labels = list(value.labels)
                        properties = dict(value)
                        
                        # Create label from node type and name/title
                        label = labels[0] if labels else "Node"
                        if 'name' in properties:
                            label = f"{label}: {properties['name']}"
                        elif 'title' in properties:
                            label = f"{label}: {properties['title']}"
                        
                        nodes[node_id] = Node(
                            id=node_id,
                            properties={
                                **properties,
                                "label": label,
                                "type": labels[0] if labels else "Unknown"
                            }
                        )
                
                # Check if it's a Neo4j Relationship
                elif isinstance(value, Relationship):
                    start_id = value.start_node.element_id
                    end_id = value.end_node.element_id
                    rel_type = value.type
                    rel_properties = dict(value)
                    
                    # Add start node if not already present
                    if start_id not in nodes:
                        start_node = value.start_node
                        labels = list(start_node.labels)
                        properties = dict(start_node)
                        label = labels[0] if labels else "Node"
                        if 'name' in properties:
                            label = f"{label}: {properties['name']}"
                        elif 'title' in properties:
                            label = f"{label}: {properties['title']}"
                        
                        nodes[start_id] = Node(
                            id=start_id,
                            properties={
                                **properties,
                                "label": label,
                                "type": labels[0] if labels else "Unknown"
                            }
                        )
                    
                    # Add end node if not already present
                    if end_id not in nodes:
                        end_node = value.end_node
                        labels = list(end_node.labels)
                        properties = dict(end_node)
                        label = labels[0] if labels else "Node"
                        if 'name' in properties:
                            label = f"{label}: {properties['name']}"
                        elif 'title' in properties:
                            label = f"{label}: {properties['title']}"
                        
                        nodes[end_id] = Node(
                            id=end_id,
                            properties={
                                **properties,
                                "label": label,
                                "type": labels[0] if labels else "Unknown"
                            }
                        )
                    
                    edges.append(Edge(
                        id=edge_id,
                        start=start_id,
                        end=end_id,
                        properties={
                            **rel_properties,
                            "label": rel_type,
                            "type": rel_type
                        }
                    ))
                    edge_id += 1
        
        nodes_list = list(nodes.values())
        
        if not nodes_list:
            st.warning("No nodes found in the query results.")
        else:
            st.write(f"Graph contains {len(nodes_list)} nodes and {len(edges)} edges")
            
            # Create color mapping based on node type
            def get_node_color(node):
                node_type = node["properties"].get("type", "Unknown")
                color_map = {
                    "Movie": "#e91e63",
                    "Person": "#2196f3",
                    "User": "#4caf50",
                    "Genre": "#ff9800",
                    "Actor": "#9c27b0",
                    "Director": "#f44336",
                }
                return color_map.get(node_type, "#607d8b")
            
            # Create the widget with styling
            widget = StreamlitGraphWidget(
                nodes_list,
                edges,
                node_label_mapping="label",
                node_color_mapping=get_node_color,
                edge_label_mapping=lambda e: e["properties"]["label"],
            )
            
            # Display the graph
            widget.show(
                directed=True,
                graph_layout=Layout.ORGANIC,
                sidebar={"enabled": True, "start_with": "Data"},
                overview=True
            )

except Exception as e:
    st.error(f"Error: {str(e)}")
    st.write("Please check your Neo4j connection details and query.")
    st.exception(e)

# Footer
st.sidebar.markdown("---")
st.sidebar.info("""
**Database Info:**
- URI: demo.neo4jlabs.com:7473
- Database: recommendations
- User: recommendations
""")
