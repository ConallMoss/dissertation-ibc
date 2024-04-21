from src.utils.typing_utils import *
from src.utils.component_utils import *
from src.utils.bfs_utils import *
from src.utils.dependency_utils import *

from collections import defaultdict, deque
from typing import Optional
import copy


def iCentral(G: Graph, BC: dict[Node, float], e: Edge) -> dict[Node, float]:
    
    V_ins: list[Node] = [] #Check if either node is new to the graph
    for v in e:
        if v not in G.nodes:
            V_ins.append(v)

    v1, v2 = e
    G.add_nodes_from(V_ins)
    for v in V_ins:
        BC[v] = BC.get(v, 0) #* Initialise into dictionary for new nodes
    subgraphs: Optional[tuple[Graph, Graph]] = find_bridge_subgraphs(G, e)
    G.add_edge(v1, v2)

    if (subgraphs):
        v_s, v_t = e 
        subgraph_s, subgraph_t = subgraphs
        node_pair_dependency_s: dict[Node, float] = find_node_pair_dependencies(subgraph_s, v_s)
        node_pair_dependency_t: dict[Node, float] = find_node_pair_dependencies(subgraph_t, v_t)
        for n_s in subgraph_s.nodes:
            BC[n_s] += len(subgraph_t) * node_pair_dependency_s[n_s]
        for n_t in subgraph_t.nodes:
            BC[n_t] += len(subgraph_s) * node_pair_dependency_t[n_t]

    else:
        all_bicons: list[set[Node]] = find_biconnected_components(G)
        all_articulation_points: set[Node] = find_articulation_points(G)

        #* We only care about the bicon with our new edge
        bicon_new: Graph = G.subgraph(find_bicon_with_edge(all_bicons, e)).copy() #* B_e'
        bicon_old: Graph = copy.deepcopy(bicon_new) #* B_e in paper
        bicon_old.remove_edge(v1, v2)

        our_articulation_points: set[Node] = all_articulation_points.intersection(bicon_new.nodes)
        articulation_subgraph_size: dict[Node, int] = find_connected_subgraph_size(G, our_articulation_points, bicon_new.nodes)

        #* Line 4:
        distances_v1: dict[Node, int] = bfs_distances(bicon_old, v1)
        distances_v2: dict[Node, int] = bfs_distances(bicon_old, v2)

        #* Line 7:
        recalculation_queue: deque[Node] = deque() #Queue
        for s in bicon_old.nodes: 
            #* Check if ends of the edge are at different distances from edge endpoints
            #* i.e. if not, then edge would not be used
            if distances_v1[s] != distances_v2[s]: 
                recalculation_queue.append(s)
        
        bicon_old_adj: GraphAdj = bicon_old._adj
        bicon_new_adj: GraphAdj = bicon_new._adj

        #* Show number of nodes to recalculate over
        print(f"RS: {len(recalculation_queue)}")

        #* Line 10: 
        for s in recalculation_queue:
            shortest_paths_old, preds_old, ordered_nodes_old = bfs_brandes(bicon_old_adj, s) #* σ_s, P_s
            pair_dependency_old: dict[Node, float] = defaultdict(float) #* δ_sdot
            external_dependency_old: dict[Node, float] = defaultdict(float) #* δ_G_sdot

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
            pair_dependency_new: dict[Node, float] = defaultdict(float) #* δ_sdot'
            external_dependency_new: dict[Node, float] = defaultdict(float) #* δ_G_sdot'

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