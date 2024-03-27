#import networkx as nx
import graphscope.nx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from collections import defaultdict
import time
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

G_base = nx.read_edgelist("../datasets/facebook_combined.txt")
G = G_base
e = pick_random_nonedge(G_base)
print(e)

# %%
#* Real time iCentral
G = G_base.copy()
bce_initial = defaultdict(float)
s = time.perf_counter()
x = iCentral(G, bce_initial, e)
print("Real time iCentral:")
print(time.perf_counter() - s)

# %%
#* Real time LeeBCC
G = G_base.copy()
bce_initial = defaultdict(float)
s = time.perf_counter()
x = LeeBCC(G, bce_initial, e)
print("Real time LeeBCC:")
print(time.perf_counter() - s)