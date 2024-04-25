import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
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

if __name__ == "__main__":
    # G2 = nx.read_edgelist("./datasets/facebook_combined.txt")
    # e = ('693', '2379')

    G2 = nx.read_edgelist("../datasets/slashdot-threads/out.slashdot-threads", nodetype=str, comments="%", data=False)
    e = ('1095', '3289')

    # G2 = nx.read_edgelist("./datasets/pajek-erdos/out.pajek-erdos", nodetype=str, comments="%", data=False)
    # e = ('760', '229')

    print(e)
    print(G2.number_of_nodes())

    #* Real time iCentral_p
    print("Running iCentral_p:")
    G = G2.copy()
    bce_initial = defaultdict(float)
    s = time.perf_counter()
    x = iCentral_p(G, bce_initial, e, num_cores=32)
    print("Real time Parallel iCentral:")
    print(time.perf_counter() - s)
    print("")

    # #* Real time LeeBCC
    # print("Running LeeBCC:")
    # G = G2.copy()
    # bce_initial = defaultdict(float)
    # s = time.perf_counter()
    # x = LeeBCC(G, bce_initial, e)
    # print("Real time LeeBCC:")
    # print(time.perf_counter() - s)
    # print("")

    #* Real time iCentral
    print("Running iCentral:")
    G = G2.copy()
    bce_initial = defaultdict(float)
    s = time.perf_counter()
    y = iCentral(G, bce_initial, e)
    print("Real time iCentral:")
    print(time.perf_counter() - s)