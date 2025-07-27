import osmnx as ox
import networkx as nx

def find_real_road_route(pickup_point, destination_point):
    """
    pickup_point & destination_point: GEOSGeometry Point (lon, lat)
    Returns list of (lat, lon) tuples representing the road path.
    """
    # Convert to (lat, lon)
    pickup = (pickup_point.y, pickup_point.x)
    destination = (destination_point.y, destination_point.x)

    # Get road network from OpenStreetMap around pickup
    G = ox.graph_from_point(pickup, dist=3000, network_type='drive')

    # Find nearest nodes
    orig_node = ox.nearest_nodes(G, pickup[1], pickup[0])
    dest_node = ox.nearest_nodes(G, destination[1], destination[0])

    # Dijkstra path
    route = nx.shortest_path(G, orig_node, dest_node, weight="length")

    # Convert node path to (lat, lon)
    route_coords = [(G.nodes[n]["y"], G.nodes[n]["x"]) for n in route]
    return route_coords
