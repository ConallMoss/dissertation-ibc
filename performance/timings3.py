# %%
from pathlib import Path
import sys
parent_dir = str(Path().resolve().parents[0])
sys.path.insert(0, parent_dir)

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
G2 = nx.read_edgelist("../datasets/facebook_combined.txt")
e = ('693', '2379')

#G2 = nx.read_edgelist("../datasets/slashdot-threads/out.slashdot-threads", nodetype=str, comments="%", data=False)
#e = ('1095', '3289')

bc1 = defaultdict(float)
# %%
s = time.perf_counter()
bc_c = iCentral(G2, bc1, e)
print(time.perf_counter() - s)
# %%
s = time.perf_counter()
#bc_i = .betweenness()
print(time.perf_counter() - s)
# %%
with cProfile.Profile() as pr:
    x = iCentral(G2, bc1, e)
    stats = pstats.Stats(pr)
    print("iCentral:")
    stats.sort_stats(SortKey.CUMULATIVE).print_stats()
# %%
