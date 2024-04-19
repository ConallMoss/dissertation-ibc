from src.LeeBCC import *
from src.iCentral_p import *
# %%

if __name__ == "__main__":
    G = nx.Graph([(0,1), (1,2), (2,3)])
    e = (0,3)

    bc = nx.betweenness_centrality(G, endpoints=False, normalized=False)

    bc_iCentral = iCentral_p(G, bc, e, PROCESSES=4)
    bc_new = nx.betweenness_centrality(G, endpoints=False, normalized=False)

    print(bc_iCentral)
    print(bc_new)