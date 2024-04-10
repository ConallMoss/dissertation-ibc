from src.utils.my_imports import *
from src.utils.general import *

   
def find_edge_pair_dependencies(G: Graph, s: Node) -> dict[Edge, float]:
    """
    Finds edge pair dependencies ($δ^G_{s,⋅}$, effect node has on each edge) of node for each edge in graph
    (Using definition from LeeBCC paper)
    """
    S: deque[Node] = deque() # Stack
    P: dict[Node, list[Node]] = defaultdict(list) #empty list for each W \in V
    σ: dict[Node, int] = defaultdict(int); σ[s] = 1
    d: dict[Node, int] = defaultdict(lambda: -1); d[s] = 0
    Q: deque[Node] = deque((s,)) #Queue
    while len(Q):
        v: Node = Q.popleft()
        S.append(v)
        for w in G[v]:
            #w found for first time?
            if d[w] < 0:
                Q.append(w)
                d[w] = d[v] + 1
            #shortest path to w is via v?
            if d[w] == d[v] + 1:
                σ[w] = σ[w] + σ[v]
                P[w].append(v)

    δ_v = defaultdict(float)
    δ_e: dict[Edge, float] = {(e if e[0] <= e[1] else (e[1], e[0])): 0.0 for e in G.edges}

    #S returns vertices in non-increasing distance order from s
    while len(S):
        w: Node = S.pop()
        for v in P[w]:
            δ_v[v] += σ[v] / σ[w] * (1 + δ_v[w])
            δ_e[(v,w) if v <= w else (w,v)] += σ[v] / σ[w] * (1 + δ_v[w]) #formlua from paper

    return δ_e  

def find_node_pair_dependencies(G: Graph, s: Node) -> dict[Node, float]:
    """
    Finds node source dependencies, using Brandes method
    """
    S: deque[Node] = deque() # Stack
    P: dict[Node, list[Node]] = defaultdict(list) #empty list for each W \in V
    σ: dict[Node, int] = defaultdict(int); σ[s] = 1
    d: dict[Node, int] = defaultdict(lambda: -1); d[s] = 0
    Q: deque[Node] = deque((s,)) #Queue
    while len(Q):
        v: Node = Q.popleft()
        S.append(v)
        for w in G[v]:
            #w found for first time?
            if d[w] < 0:
                Q.append(w)
                d[w] = d[v] + 1
            #shortest path to w is via v?
            if d[w] == d[v] + 1:
                σ[w] = σ[w] + σ[v]
                P[w].append(v)

    δ_v = defaultdict(float)

    #S returns vertices in non-increasing distance order from s
    while len(S):
        w: Node = S.pop()
        for v in P[w]:
            δ_v[v] += σ[v] / σ[w] * (1 + δ_v[w])

    return δ_v