# %%
# from pathlib import Path
# import sys
# parent_dir = str(Path().resolve().parents[0])
# sys.path.insert(0, parent_dir)

import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
import time
import random
import cProfile, pstats

def pick_random_nonedge(G, seed=None):
    if seed is not None:
        random.seed(seed)
    node1 = random.choice(list(G.nodes()))
    possible_nodes = set(G.nodes())
    neighbours = set(G[node1]).union({node1})
    possible_nodes.difference_update(neighbours)
    node2 = random.choice(list(possible_nodes))
    return node1, node2

# %%
if __name__ == "__main__":
    # G2 = nx.read_edgelist("./datasets/facebook_combined.txt")
    # e = ('693', '2379')

    G2 = nx.read_edgelist("./datasets/slashdot-threads/out.slashdot-threads", nodetype=str, comments="%", data=False)
    e = ('1095', '3289')

    print(e)
    print(G2.number_of_nodes())

    bc1 = defaultdict(float)

    with cProfile.Profile() as pr:
        x = LeeBCC(G2, bc1, e)
        stats = pstats.Stats(pr)
        print("LeeBCC:")
        stats.sort_stats(pstats.SortKey.CUMULATIVE).print_stats()