import sys
import networkx as nx
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

def get_dataset(name):
    return nx.read_edgelist(f"../datasets/{name}/out.{name}", nodetype=int, comments="%", data=False)

def get_lcc(G):
    return max(nx.connected_components(G), key=len)

dataset = sys.argv[1]
G_base = get_dataset(dataset)

edges = []
counts = [[], []]

runs = int((sys.argv[2:3] or [0])[0])

for i in range(runs):
    e = pick_random_nonedge(G_base)
    edges.append(e)
    #* Real time iCentral
    G = G_base.copy()
    bce_initial = defaultdict(float)
    s = time.perf_counter()
    x = iCentral(G, bce_initial, e)
    #print("Real time iCentral:")
    counts[0].append(time.perf_counter() - s)

    #* Real time LeeBCC
    G = G_base.copy()
    bce_initial = defaultdict(float)
    s = time.perf_counter()
    x = LeeBCC(G, bce_initial, e)
    #print("Real time LeeBCC:")
    counts[1].append(time.perf_counter() - s)

print("dataset:")
print(dataset)
print("edges:")
print(edges)
print("Average iCentral:")
print(sum(counts[0])/runs)
print("Average LeeBCC:")
print(sum(counts[1])/runs)
print("Real times iCentral:")
print(counts[0])
print("Real times LeeBCC: ")
print(counts[1])