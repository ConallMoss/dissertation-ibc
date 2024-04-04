# %%
from pathlib import Path
import sys
parent_dir = str(Path().resolve().parents[0])
sys.path.insert(0, parent_dir)

import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
import cProfile, pstats
from pstats import SortKey
import random
import time

# %%
G = nx.Graph([(0,1), (1,2), (2,3), (3,0), (4,5), (5,6), (6,7), (7,4)])

Graph = nx.Graph
Node = int
Edge = tuple[Node, Node]

def norm(e: tuple[Node, Node]) -> tuple[Node, Node]:
    """
    Normalises edge so e[0] <= e[1]
    """
    return (e if e[0] <= e[1] else (e[1], e[0])) 

def true_bce(G):
    bce = nx.edge_betweenness_centrality(G, normalized=False)
    return {norm(k): v for k, v in bce.items()}

def dotest_LeeBCC(G: Graph, e: Edge, v_ins=None):
    #* Arrange
    bce_initial = true_bce(G)
    G2 = G.copy()
    G2.add_nodes_from(v_ins)
    G2.add_edge(*e)
    bce_new = true_bce(G2)

    #*Act
    bce_LeeBCC = LeeBCC(G, bce_initial, e, v_ins)

    return bce_new, bce_LeeBCC
# %%
a, b = dotest_LeeBCC(G, (7, 8), [8])
# %%
