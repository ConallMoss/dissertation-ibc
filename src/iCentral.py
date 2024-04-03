from src.utils.my_imports import *
from src.utils.general import *
from src.utils.bicon_utils import *
from src.utils.bfs_utils import *


def iCentral(G: Graph, BC: dict[Node, float], e: Edge) -> dict[Node, float]:
    v1, v2 = e
    G.add_edge(v1, v2)
    all_bicons = find_biconnected_components(G)
    all_articulation_points = find_articulation_points(G)

    #* We only care about the bicon with our new edge
    bicon_new = G.subgraph(find_bicon_with_edge(all_bicons, e)).copy() #* B_e'
    bicon_old = deepcopy(bicon_new) #* B_e in paper
    bicon_old.remove_edge(v1, v2)

    our_articulation_points = all_articulation_points.intersection(bicon_new.nodes)
    articulation_subgraph_size = find_connected_subgraph_size(G, our_articulation_points, bicon_new.nodes)

    #* Line 4:
    d1 = bfs_distances(bicon_old, v1)
    d2 = bfs_distances(bicon_old, v2)

    #* Line 7:
    Q = deque() #Queue
    for s in bicon_old.nodes: 
        #* Check if ends of the edge are at different distances from edge endpoints
        #* i.e. if not, then edge would not be used
        if d1[s] != d2[s]: 
             Q.append(s)
    
    bicon_old_adj = bicon_old._adj
    bicon_new_adj = bicon_new._adj

    #* Line 10: 
    for s in Q:
        shortest_paths_old, preds_old, ordered_nodes_old = bfs_brandes(bicon_old_adj, s) #* σ_s, P_s
        pair_dependency_old = defaultdict(float) #* δ_sdot
        external_dependency_old = defaultdict(float) #* δ_G_sdot

        for w in ordered_nodes_old:
            if (s in our_articulation_points) and (w in our_articulation_points):
                external_dependency_old[w] = articulation_subgraph_size[s] * articulation_subgraph_size[w] 

            for p in preds_old[w]:
                pair_dependency_old[p] += shortest_paths_old[p] / shortest_paths_old[w] * (1 + pair_dependency_old[w])
                if (s in our_articulation_points):
                    external_dependency_old[p] += external_dependency_old[w] * shortest_paths_old[p] / shortest_paths_old[w]

            if w != s:
                BC[w] -= pair_dependency_old[w] / 2

            if (s in our_articulation_points):
                BC[w] -= pair_dependency_old[w] * articulation_subgraph_size[s]
                BC[w] -= external_dependency_old[w] / 2

        #* Line 26:
        shortest_paths_new, preds_new, ordered_nodes_new = bfs_brandes(bicon_new_adj, s) #* σ_s', P_s'
        pair_dependency_new = defaultdict(float) #* δ_sdot'
        external_dependency_new = defaultdict(float) #* δ_G_sdot'

        for w in ordered_nodes_new:
            if (s in our_articulation_points) and (w in our_articulation_points): 
                external_dependency_new[w] = articulation_subgraph_size[s] * articulation_subgraph_size[w]

            for p in preds_new[w]:
                pair_dependency_new[p] += shortest_paths_new[p] / shortest_paths_new[w] * (1 + pair_dependency_new[w])
                if (s in our_articulation_points):
                    external_dependency_new[p] += external_dependency_new[w] * shortest_paths_new[p] / shortest_paths_new[w]

            if w != s:
                BC[w] += pair_dependency_new[w] / 2

            if (s in our_articulation_points):
                BC[w] += pair_dependency_new[w] * articulation_subgraph_size[s]
                BC[w] += external_dependency_new[w] / 2

    return BC