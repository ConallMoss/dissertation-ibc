import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
import time
import random
import os
import argparse
import copy
from datetime import datetime
from memory_profiler import memory_usage

start_time = time.perf_counter()

def pick_random_safe_edge(G, edges=None):
    if edges is None:
        edges = list(G.edges)
    G2 = G.copy()
    edges = list(G.edges)
    e = random.choice(edges)
    G2.remove_edge(e[0], e[1])
    #Greedy edge removal
    while len(list(nx.connected_components(G2))) != 1:
        G2.add_edge(e[0], e[1])
        e = random.choice(edges)
        G2.remove_edge(e[0], e[1])
    return G2, e

def get_dataset(name):
    return nx.read_edgelist(f"./datasets/{name}/out.{name}", nodetype=str, comments="%", data=False)

def get_lcc(G):
    G2 = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    G2.remove_edges_from(nx.selfloop_edges(G2))
    return G2

def get_bcc(G):
    return G.subgraph(max(nx.biconnected_components(G), key=len)).copy()

parser = argparse.ArgumentParser()
parser.add_argument("dataset", help="Dataset to use", type=str)
parser.add_argument("--max_runs", "-r", help="max number of runs", type=int, default=100)
parser.add_argument("--cores", "-c", help="how many cores to run on", type=int, default=2)

random.seed(42)
args = parser.parse_args()

if __name__ == "__main__":
    
    dataset = args.dataset
    cores = args.cores

    max_runs = args.max_runs
    max_secs = 40000

    print(datetime.now())
    print(f"{dataset=}")
    print(f"{max_runs=}")
    print(f"{max_secs=}")
    print(f"{cores=}")
    #if prog == "iCentral_p":
    #    print(f"processes={os.cpu_count()}")
    print("")


    subgraping = "lcc"
    
    subgraph_funcs = {
        "lcc": get_lcc,
        "bcc": get_bcc
    }
    subgraphing_func = subgraph_funcs[subgraping]

    start_time = time.perf_counter()
    G_base = subgraphing_func(get_dataset(dataset))
    graph_read_time = time.perf_counter() - start_time
    print(f"graph size: N={G_base.number_of_nodes()}, E={G_base.number_of_edges()}")
    print(f"Subgraphing: {subgraping}")
    print("Graph read time:")
    print(graph_read_time)
    print("")

    curr_mem = memory_usage(-1)[0]
    print("Current memory usage:")
    print(f"M: {curr_mem}")

    print("Run times:")

    run = 0
    while ((time.perf_counter()-start_time)<max_secs) and (run < max_runs):
        run += 1
        G, e = pick_random_safe_edge(G_base)
        
        G = copy.deepcopy(G_base)
        initial = defaultdict(float)
        s = time.perf_counter()
        x = iCentral_p(G, initial, e, num_cores=cores)


        print(f"T: {time.perf_counter()-s}", flush=True)
        print("")

