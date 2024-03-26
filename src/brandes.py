from src.utils.my_imports import *
from src.utils.general import *

def brandes(G: Graph) -> dict[Node, float]:
    """Implementation of Brandes algorithm for generic comparison"""
    #* Uses naming convention from Brandes paper, which may differ from my other BC implementations
    C = defaultdict(float)
    V = G.nodes
    for s in V:
        S = deque() #Stack
        P = defaultdict(list)
        σ = defaultdict(int); σ[s] = 1
        d = defaultdict(lambda: -1); d[s] = 0
        Q = deque((s,)) #Queue
        while len(Q):
            v = Q.popleft()
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
    
        δ = defaultdict(float)
        #S returns vertices in non-increasing distance order from s
        while len(S):
            w = S.pop()
            for v in P[w]:
                δ[v] = δ[v] + σ[v] / σ[w] * (1 + δ[w])
            if w != s:
                C[w] = C[w] + δ[w]
    return C
