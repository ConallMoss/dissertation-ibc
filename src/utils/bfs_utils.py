from src.utils.my_imports import *
from src.utils.general import *

def bfs_distances(G: Graph, s: Node) -> dict[Node, int]: 
    """Finds node distances using BFS"""
    distance = defaultdict(int)
    distance[s] = 0
    Q = deque((s,))
    while Q:
        n = Q.popleft()
        for i in G[n]:
            if i not in distance:
                distance[i] = distance[n] + 1
                Q.append(i)
    return distance

def bfs_brandes(G: Graph, s: Node) -> tuple[dict[Node, int], dict[Node, set[Node]], list[Node]]:
    """Find node's no. shortest paths, parents and reverse bfs order from given node"""
    distance = {s: 0}
    parents = defaultdict(list)
    sigma = defaultdict(int); sigma[s] = 1
    Q = deque((s,))
    while Q:
        n = Q.popleft()
        d = distance[n]
        for i in G[n]:
            if i not in distance:
                distance[i] = d + 1
                Q.append(i)
                parents[i].append(n)
                sigma[i] += sigma[n]
            elif distance[i] == d + 1:
                parents[i].append(n)
                sigma[i] += sigma[n]
    return sigma, parents, distance.keys().__reversed__()