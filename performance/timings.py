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

"""
from pathlib import Path
import sys
parent_dir = str(Path().resolve().parents[0])
sys.path.insert(0, parent_dir)
"""

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
#e = pick_random_nonedge(G_base)
e = ('693', '2379')#('1095', '3289')

#* Performance tests:

# %%
#* Profile iCentral
G = G_base.copy()
bce_initial = defaultdict(float)
#e = ('2289', '2510')
with cProfile.Profile() as pr:
    x = iCentral(G, bce_initial, e)
    stats = pstats.Stats(pr)
    print("Profile iCentral:")
    stats.sort_stats(SortKey.CUMULATIVE).print_stats()

# %%
#* Profile LeeBCC
G = G_base.copy()
bce_initial = defaultdict(float)
with cProfile.Profile() as pr:
    x = LeeBCC(G, bce_initial, e)
    stats = pstats.Stats(pr)
    print("Profile LeeBCC:")
    stats.sort_stats(SortKey.CUMULATIVE).print_stats()

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
# %%

# %%
