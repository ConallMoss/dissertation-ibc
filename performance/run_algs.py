import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
import time

G2 = nx.read_edgelist("./datasets/facebook_combined.txt")
e = ('692', '2378')


print("Running LeeBCC:")
G = G2.copy()
bce_initial = defaultdict(float)
s = time.perf_counter()
x = LeeBCC(G, bce_initial, e)
print("Real time LeeBCC:")
print(time.perf_counter() - s)
print("")


#* Real time iCentral
print("Running iCentral:")
G = G2.copy()
bce_initial = defaultdict(float)
s = time.perf_counter()
y = iCentral(G, bce_initial, e)
print("Real time iCentral:")
print(time.perf_counter() - s)