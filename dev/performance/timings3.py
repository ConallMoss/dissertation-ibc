# %%
from pathlib import Path
import sys
parent_dir = str(Path().resolve().parents[1])
print(parent_dir)
sys.path.insert(0, parent_dir)
# %%
import networkx as nx
from src.LeeBCC import LeeBCC
from src.iCentral import iCentral
from src.iCentral_p import iCentral_p
from collections import defaultdict
import cProfile, pstats
from pstats import SortKey
import random
import time
import logging
import sys
from pytest import approx
import math

# %%
#G2 = nx.read_edgelist("./datasets/facebook_combined.txt")
#e = ('693', '2379')

#G2 = nx.read_edgelist("../datasets/slashdot-threads/out.slashdot-threads", nodetype=str, comments="%", data=False)
#e = ('1095', '3289')

#G2 = nx.read_edgelist("../datasets/pajek-erdos/out.pajek-erdos", nodetype=str, comments="%", data=False)
#e = ('760', '229')

G2 = nx.read_edgelist("../../datasets/facebook-combined/out.facebook-combined")
e = ('0', '124')

bc1 = defaultdict(float)
# %%
# %%
# s = time.perf_counter()
# bc_c = iCentral(G2, bc1, e)
# print(time.perf_counter() - s)
# %%
# s = time.perf_counter()
# #bc_i = .betweenness()
# print(time.perf_counter() - s)
# %%
with cProfile.Profile() as pr:
    x = iCentral(G2, bc1, e)
    stats = pstats.Stats(pr)
    print("LeeBCC:")
    stats.sort_stats(SortKey.CUMULATIVE).print_stats(100)
# %%
with cProfile.Profile() as pr:
    x = LeeBCC(G2, bc1, e)
    stats = pstats.Stats(pr)
    print("LeeBCC:")
    stats.sort_stats(SortKey.CUMULATIVE).print_stats(100)

with cProfile.Profile() as pr:
    x = iCentral_p(G2, bc1, e, 4)
    stats = pstats.Stats(pr)
    print("iCentral_p:")
    stats.sort_stats(SortKey.CUMULATIVE).print_stats(100)
# %%
