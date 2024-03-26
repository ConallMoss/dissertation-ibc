from src.utils.my_imports import *
from src.utils.general import *

def find_biconnected_components(G: Graph) -> list[set[Node]]: 
    """
    Returns all biconnected components of graph
    """
    #* We currently just use provided NetworkX method, but could use own implementation
    bicons = list(nx.biconnected_components(G)) 
    return bicons

def find_articulation_points(G: Graph) -> set[Node]:
    """
    Finds all articulation points of graph
    """
    #* We currently just use provided NetworkX method, but could use own implementation
    articulation_points = set(nx.articulation_points(G))
    return articulation_points

def find_bicon_with_edge(bicons: list[set[Node]], e: Edge) -> set[Node]: 
    """Finds and returns bicon from given bicon contains edge"""
    v1, v2 = e
    for bicon in bicons:
        if (v1 in bicon) and (v2 in bicon):
            return bicon
        
def find_bicon_with_node(bicons: list[set[Node]], n: Node) -> set[Node]:
    """Finds and returns bicon from given bicon contains node"""
    for bicon in bicons:
        if n in bicon:
            return bicon
        

def find_connected_subgraph_size(G: Graph, our_ap: set[Node], our_bicon: set[Node]) -> dict[Node, int]:
    """Finds size of full subgraph connected to bicon through each articulation point of bicon"""
    #TODO: Copy bfs, blacklist bicon edges/nodes
    G2 = G.copy()
    for ap in our_ap:
        #* Disconnect APs from our bicon
        G2.remove_edges_from([(n,ap) for n in G[ap] if n in our_bicon])
    #* Find lengths of full attached graphs
    return {ap: len(nx.node_connected_component(G2, ap))-1 for ap in our_ap}