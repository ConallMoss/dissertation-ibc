import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
import cProfile, pstats
from pstats import SortKey
import random
import time
import logging
import sys

if __name__ == "__main__":
    
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

    #G_base = nx.read_edgelist("./datasets/facebook_combined.txt")
    G_base =  nx.erdos_renyi_graph(256, 0.5, seed=123, directed=False)
    G = G_base
    e = pick_random_nonedge(G_base)
    #e = ('693', '2379')#('1095', '3289')
    print(e)

    #* Profile iCentral
    G = G_base.copy()
    bce_initial = defaultdict(float)
    #e = ('2289', '2510')
    with cProfile.Profile() as pr:
        x = iCentral_p(G, bce_initial, e, PROCESSES=16)
        stats = pstats.Stats(pr)
        print("Profile iCentral:")
        stats.sort_stats(SortKey.CUMULATIVE).print_stats()