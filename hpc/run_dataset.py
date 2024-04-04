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

start_time = time.perf_counter()

def pick_random_new_nonedge(G, seed=None, G_nodes=None):
    if G_nodes is None:
        G_nodes = set(G.nodes())
    if seed is not None:
        random.seed(seed)
    node1 = random.choice(list(G_nodes))
    neighbours = set(G[node1]).union({node1})
    G_nodes -= neighbours
    node2 = random.choice(list(G_nodes))
    return node1, node2

def get_dataset(name):
    if name == "facebook_combined":
        return nx.read_edgelist(f"../datasets/facebook_combined.txt", nodetype=int, comments="%", data=False)
    return nx.read_edgelist(f"../datasets/{name}/out.{name}", nodetype=int, comments="%", data=False)

def get_lcc(G):
    return G.subgraph(max(nx.connected_components(G), key=len)).copy()

parser = argparse.ArgumentParser()
parser.add_argument("dataset", help="Dataset to use", type=str)
parser.add_argument("--max_runs", "-r", help="max number of runs", type=int, default=1)
parser.add_argument("--prog", "-p", help="which program to run", type=str, default="iCentral")

args = parser.parse_args()

if __name__ == "__main__":
    
    dataset = args.dataset
    prog = args.prog

    max_runs = args.max_runs
    max_secs = 20000

    print(datetime.now())
    print(f"{dataset=}")
    print(f"{prog=}")
    print(f"{max_runs=}")
    print(f"{max_secs=}")
    if prog == "iCentral_p":
        print(f"processes={os.cpu_count()}")
    print("")

    
    funcs = {
        "iCentral": iCentral,
        "iCentral_p": iCentral_p,
        "LeeBCC": LeeBCC
    }
    func = funcs[prog]




    start_time = time.perf_counter()
    G_base = get_lcc(get_dataset(dataset))
    graph_read_time = time.perf_counter() - start_time

    print("Graph read time:")
    print(graph_read_time)
    print("")

    print("Run times:")

    run = 0
    while ((time.perf_counter()-start_time)<max_secs) and (run < max_runs):
        run += 1
        e = pick_random_new_nonedge(G_base)
        
        G = copy.deepcopy(G_base)
        initial = defaultdict(float)
        s = time.perf_counter()
        x = func(G, initial, e)
        print(time.perf_counter()-s)

