import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
import time
import random
import os

start_time = time.perf_counter()

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
    if name == "facebook_combined":
        return nx.read_edgelist(f"../datasets/facebook_combined.txt", nodetype=int, comments="%", data=False)
    return nx.read_edgelist(f"../datasets/{name}/out.{name}", nodetype=int, comments="%", data=False)

def get_lcc(G):
    return G.subgraph(max(nx.connected_components(G), key=len)).copy()


if __name__ == "__main__":
    
    dataset = "ego-facebook"

    max_runs = 1000
    max_secs = 20000

    print(f"{dataset=}")
    print(f"{max_runs=}")
    print(f"{max_secs=}")
    print("")

    s = time.perf_counter()
    G_base = get_lcc(get_dataset(dataset))
    graph_read_time = time.perf_counter() - s

    edges = []
    counts = [[], [], []]

    run = 0
    while ((time.perf_counter()-s)<max_secs) and (run < max_runs):
        run += 1
        #print(f"{run=}")
        e = pick_random_nonedge(G_base)
        edges.append(e)
        #print(f"{e=}")
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

        #* Real time iCentral_p
        G = G_base.copy()
        bce_initial = defaultdict(float)
        s = time.perf_counter()
        x = iCentral_p(G, bce_initial, e, PROCESSES=None)
        counts[2].append(time.perf_counter() - s)

    print("dataset:")
    print(dataset)
    print("")
    print("Graph read time:")
    print(graph_read_time)
    print("")
    print("edges:")
    print(edges)
    print("")
    print("processes")
    print(os.cpu_count())
    print("")
    print("runs")
    print(run)
    print("")
    if run != 1:
        print("Average iCentral:")
        print(sum(counts[0])/run)
        print("")
        print("Average LeeBCC:")
        print(sum(counts[1])/run)
        print("")
        print("Average iCentral_p:")
        print(sum(counts[2])/run)
        print("")
    print("Real times iCentral:")
    print(counts[0])
    print("")
    print("Real times LeeBCC: ")
    print(counts[1])
    print("")
    print("Real times iCentral_p: ")
    print(counts[2])