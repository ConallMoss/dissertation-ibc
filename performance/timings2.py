import sys
import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
import time
import random
import logging

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel("INFO")

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

dataset = "pajek-erdos"
G_base = get_dataset(dataset)

e = pick_random_nonedge(G_base)

print(f"{dataset=}")
print(f"{e=}")

#* Real time iCentral_p
G = G_base.copy()
bc_initial = defaultdict(float)
s = time.perf_counter()
x = iCentral_p(G, bc_initial, e)
print("Real time iCentral_p:")
print(time.perf_counter() - s)

e = pick_random_nonedge(G_base)
#* Real time iCentral
G = G_base.copy()
bc_initial = defaultdict(float)
s = time.perf_counter()
x = iCentral(G, bc_initial, e)
print("Real time iCentral:")
print(time.perf_counter() - s)

#* Real time LeeBCC
G = G_base.copy()
bce_initial = defaultdict(float)
s = time.perf_counter()
x = LeeBCC(G, bce_initial, e)
print("Real time LeeBCC:")
print(time.perf_counter() - s)