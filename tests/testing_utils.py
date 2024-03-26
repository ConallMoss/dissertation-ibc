import networkx as nx
from src.iCentral import *
from src.LeeBCC import *
import random

def pick_random_nonedge(G, seed=None):
    if seed is not None:
        random.seed(seed)
    node1 = random.choice(list(G.nodes()))
    possible_nodes = set(G.nodes())
    neighbours = set(G[node1]).union({node1})
    possible_nodes.difference_update(neighbours)
    node2 = random.choice(list(possible_nodes))
    return node1, node2

#* iCentral:

def true_bc(G):
    return nx.betweenness_centrality(G, normalized=False, endpoints=False)

def dotest_iCentral(G: Graph, e: Edge):
    #* Arrange
    bc_initial = true_bc(G)
    G2 = G.copy()
    G2.add_edge(*e)
    bc_new = true_bc(G2)

    #*Act
    bc_iCentral = iCentral(G, bc_initial, e)

    return bc_new, bc_iCentral

#* LeeBCC:

def norm(e: tuple[Node, Node]) -> tuple[Node, Node]:
    """
    Normalises edge so e[0] <= e[1]
    """
    return (e if e[0] <= e[1] else (e[1], e[0])) 

def true_bce(G):
    bce = nx.edge_betweenness_centrality(G, normalized=False)
    return {norm(k): v for k, v in bce.items()}

def dotest_LeeBCC(G: Graph, e: Edge):
    #* Arrange
    bce_initial = true_bce(G)
    G2 = G.copy()
    G2.add_edge(*e)
    bce_new = true_bce(G2)

    #*Act
    bce_LeeBCC = LeeBCC(G, bce_initial, e)

    return bce_new, bce_LeeBCC