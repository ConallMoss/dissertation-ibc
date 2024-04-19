from src.utils.typing_utils import *
from collections import defaultdict, deque
from typing import Iterable

def bfs_distances(G: Graph, s: Node) -> dict[Node, int]: 
    """Finds node distances using BFS"""
    distance: dict[Node, int] = defaultdict(int)
    distance[s] = 0
    Q: deque = deque((s,))
    while Q:
        n: Node = Q.popleft()
        for i in G[n]:
            if i not in distance:
                distance[i] = distance[n] + 1
                Q.append(i)
    return distance

def bfs_brandes(G: GraphAdj, s: Node) -> tuple[dict[Node, int], dict[Node, list[Node]], Iterable[Node]]:
    """Find node's no. shortest paths, parents and reverse bfs order from given node"""
    distance: dict[Node, int] = {s: 0}
    parents: dict[Node, list] = defaultdict(list)
    sigma: dict[Node, int] = defaultdict(int)
    sigma[s] = 1
    Q: deque = deque((s,))
    while Q:
        n: Node = Q.popleft()
        d: int = distance[n]
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