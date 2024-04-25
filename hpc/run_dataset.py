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

def pick_random_new_nonedge(G, seed=None, G_nodes=None):
    if G_nodes is None:
        G_nodes = set(G.nodes())
    node1 = random.choice(list(G_nodes))
    neighbours = set(G[node1]).union({node1})
    G_nodes -= neighbours
    node2 = random.choice(list(G_nodes))
    return node1, node2

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
    return G.subgraph(max(nx.connected_components(G), key=len)).copy()

def get_bcc(G):
    return G.subgraph(max(nx.biconnected_components(G), key=len)).copy()

parser = argparse.ArgumentParser()
parser.add_argument("dataset", help="Dataset to use", type=str)
parser.add_argument("--max_runs", "-r", help="max number of runs", type=int, default=1)
parser.add_argument("--prog", "-p", help="which program to run", type=str, default="iCentral")

random.seed(42)
args = parser.parse_args()

if __name__ == "__main__":
    
    dataset = args.dataset
    prog = args.prog

    max_runs = args.max_runs
    max_secs = 40000

    print(datetime.now())
    print(f"{dataset=}")
    print(f"{prog=}")
    print(f"{max_runs=}")
    print(f"{max_secs=}")
    #if prog == "iCentral_p":
    #    print(f"processes={os.cpu_count()}")
    print("")

    
    funcs = {
        "iCentral": iCentral,
        "iCentral_p": iCentral_p,
        "LeeBCC": LeeBCC
    }
    func = funcs[prog]

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
    time.sleep(0.1)
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
        if prog == "iCentral_p":
            mem, x = memory_usage(
                proc=(func, (G, initial, e), {'num_cores': 20}),
                interval=1,
                retval=True,
                include_children=True,
                multiprocess=True,
                max_iterations=1
            )
            #x = func(G, initial, e, num_cores=20)
        else:
            mem, x = memory_usage(
                proc=(func, (G, initial, e)),
                interval=1,
                retval=True,
                include_children=True,
                multiprocess=True,
                max_iterations=1
            )
            #x = func(G, initial, e)

        print(f"T: {time.perf_counter()-s}", flush=True)
        print(f"M: {max(mem)}", flush=True)
        print("")

