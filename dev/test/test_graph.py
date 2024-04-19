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
import tracemalloc


def get_dataset(name):
    return nx.read_edgelist(f"datasets/facebook_combined.txt", nodetype=str , comments="%", data=False)

def get_lcc(G):
    return G.subgraph(max(nx.connected_components(G), key=len)).copy()

def get_bcc(G):
    return G.subgraph(max(nx.biconnected_components(G), key=len)).copy()

dataset = "epinions"

tracemalloc.start()

start_time = time.perf_counter()
G_base = get_lcc(get_dataset(dataset))
graph_read_time = time.perf_counter() - start_time
print(f"graph size: N={G_base.number_of_nodes()}, E={G_base.size()}")

print("Graph read time:")
print(graph_read_time)
print("")

curr, peak = tracemalloc.get_traced_memory()

print(f"mem peak: {peak}")