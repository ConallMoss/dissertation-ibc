import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
from memory_profiler import memory_usage

def get_dataset(name):
    if name == "facebook_combined":
        return nx.read_edgelist(f"./datasets/facebook_combined.txt", nodetype=str , comments="%", data=False)
    return nx.read_edgelist(f"./datasets/{name}/out.{name}", nodetype=str, comments="%", data=False)

def get_lcc(G):
    return G.subgraph(max(nx.connected_components(G), key=len)).copy()

def get_bcc(G):
    return G.subgraph(max(nx.biconnected_components(G), key=len)).copy()

def get_bc():
    print("running get_bc")
    G2 = nx.read_edgelist("./datasets/facebook_combined.txt")
    e = ('693', '2379')

    #G2 = nx.read_edgelist("./datasets/slashdot-threads/out.slashdot-threads", nodetype=str, comments="%", data=False)
    #e = ('1095', '3289')

    #G2 = nx.read_edgelist("./datasets/pajek-erdos/out.pajek-erdos", nodetype=str, comments="%", data=False)
    #e = ('760', '229')

    print(e)
    print(G2.number_of_nodes())

    G = G2.copy()
    bce_initial = defaultdict(float)
    x = iCentral_p(G, bce_initial, e, PROCESSES=15)

    #dataset = "epinions"

    #G_base = get_bcc(get_dataset(dataset))


if __name__ == "__main__":
    print(memory_usage((get_bc), include_children=True, multiprocess=True, interval=1, timestamps=True))


