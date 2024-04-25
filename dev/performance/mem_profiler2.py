import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
from memory_profiler import memory_usage
import time

def get_dataset(name):
    return nx.read_edgelist(f"./datasets/{name}/out.{name}", nodetype=str, comments="%", data=False)

def get_lcc(G):
    return G.subgraph(max(nx.connected_components(G), key=len)).copy()

def get_bcc(G):
    return G.subgraph(max(nx.biconnected_components(G), key=len)).copy()

def get_bc(G, e, bc):
    start = time.perf_counter()
    x = iCentral(G, bc, e)
    return time.perf_counter() - start

def get_bc_p(G, e, bc):
    start = time.perf_counter()
    x = iCentral_p(G, bc, e, num_cores=20)
    return time.perf_counter() - start


if __name__ == "__main__":
    G_base = get_lcc(get_dataset("facebook-combined"))
    e = ('693', '2379')

    G = G_base.copy()
    #G.remove_edge(*e)
    bc_initial = defaultdict(float)

    mems1, t1 = memory_usage(
        proc=(get_bc, (G, e, bc_initial), {}),
        interval=1,
        retval=True
    )
    maxmem1 = max(mems1)

    G = G_base.copy()
    #G.remove_edge(*e)
    bc_initial = defaultdict(float)

    t2 = get_bc(G, e, bc_initial)

    G = G_base.copy()
    #G.remove_edge(*e)
    bc_initial = defaultdict(float)

    mems3, t3 = memory_usage(
        proc=(get_bc_p, (G, e, bc_initial), {}),
        interval=1,
        retval=True,
        include_children=True,
        multiprocess=True,
    )
    maxmem3 = max(mems3)

    G = G_base.copy()
    #G.remove_edge(*e)
    bc_initial = defaultdict(float)

    t4 = get_bc_p(G, e, bc_initial)

    print("serial")
    print(f"{maxmem1=}")
    print(f"{t1=}")
    print(f"{t2=}")

    print("parallel")
    print(f"{maxmem3=}")
    print(f"{t3=}")
    print(f"{t4=}")