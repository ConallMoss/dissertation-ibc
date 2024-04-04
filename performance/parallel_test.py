import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
import time
import random



if __name__ == "__main__":
    G2 = nx.read_edgelist("./datasets/facebook_combined.txt")
    e = ('693', '2379')

    #G2 = nx.read_edgelist("./datasets/slashdot-threads/out.slashdot-threads", nodetype=str, comments="%", data=False)
    #e = ('1095', '3289')

    # G2 = nx.read_edgelist("./datasets/pajek-erdos/out.pajek-erdos", nodetype=str, comments="%", data=False)
    # e = ('760', '229')

    print(e)
    print(G2.number_of_nodes())

    #* Real time iCentral_p
    print("Running iCentral_p: p=8")
    G = G2.copy()
    bce_initial = defaultdict(float)
    s = time.perf_counter()
    x = iCentral_p(G, bce_initial, e, PROCESSES=8)
    print("Real time Parallel iCentral:")
    print(time.perf_counter() - s)
    print("")

    #* Real time iCentral_p
    print("Running iCentral_p: p=16")
    G = G2.copy()
    bce_initial = defaultdict(float)
    s = time.perf_counter()
    x = iCentral_p(G, bce_initial, e, PROCESSES=16)
    print("Real time Parallel iCentral:")
    print(time.perf_counter() - s)
    print("")

    #* Real time iCentral_p
    print("Running iCentral_p: p=32")
    G = G2.copy()
    bce_initial = defaultdict(float)
    s = time.perf_counter()
    x = iCentral_p(G, bce_initial, e, PROCESSES=32)
    print("Real time Parallel iCentral:")
    print(time.perf_counter() - s)
    print("")