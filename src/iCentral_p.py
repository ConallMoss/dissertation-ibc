from src.utils.typing_utils import *
from src.utils.component_utils import *
from src.utils.bfs_utils import *

import multiprocessing as mp
from collections import defaultdict

def iCentral_p(G: Graph, BC: dict[Node, float], e: Edge, PROCESSES: int) -> dict[Node, float]:
    if PROCESSES is None:
        PROCESSES = mp.cpu_count()

    v1, v2 = e
    G.add_edge(v1, v2)

    all_bicons: list[set[Node]] = find_biconnected_components(G)
    all_articulation_points: set[Node] = find_articulation_points(G)

    #* We only care about the bicon with our new edge
    bicon_new: Graph = G.subgraph(find_bicon_with_edge(all_bicons, e)).copy() #* B_e'
    bicon_old: Graph= bicon_new.copy() #* B_e in paper
    bicon_old.remove_edge(v1, v2)

    our_articulation_points: set[Node] = all_articulation_points.intersection(bicon_new.nodes)
    articulation_subgraph_size: dict[Node, int] = find_connected_subgraph_size(G, our_articulation_points, bicon_new.nodes)

    #* Line 4:
    distances_v1 = bfs_distances(bicon_old, v1)
    distances_v2 = bfs_distances(bicon_old, v2)

    #* Line 7:
    #* Using threadsafe multiprocessing queue to store recalculation nodes
    recalculation_queue: mp.Queue = mp.Queue()

    for s in bicon_old.nodes: 
        #* Check if ends of the edge are at different distances from edge endpoints
        #* i.e. if not, then edge would not be used
        if distances_v1[s] != distances_v2[s]: 
             recalculation_queue.put(s)

    #* Undefault the dict - used for testing when a default dict is passed in
    for n in G.nodes:
        if n not in BC:
            BC[n] = 0

    #* Setup inputs for each call
    bicon_old_adj: GraphAdj = bicon_old._adj
    bicon_new_adj: GraphAdj = bicon_new._adj
    resources: tuple = (bicon_old_adj, bicon_new_adj, our_articulation_points, articulation_subgraph_size)
    result_queue: mp.Queue = mp.Queue() #* Threadsafe queue for main thread to read results from

    #* Spawn all processes
    for _ in range(PROCESSES-1):
        p: mp.Process = mp.Process(target=run, args=(recalculation_queue, result_queue, resources))
        p.start()

    #* We require all processes to have finished their work (which can happen in any order)
    #* Handle dictionary updates on main thread
    for _ in range(PROCESSES-1): 
        bc_update = result_queue.get(block=True) #* Blocks until data available in queue
        for k, v in bc_update.items():
            if v != 0:
                BC[k] += v
        
    return BC
 

def run(recalculation_queue: mp.Queue, result_queue: mp.Queue, resources: tuple) -> None:
        bc_upd = defaultdict(float)
        while not recalculation_queue.empty():
            s: Node = recalculation_queue.get()
            bc_upd = calculate_node_dependencies_p(s, bc_upd, *resources)
        result_queue.put(bc_upd)


def calculate_node_dependencies_p(s: Node, bc_upd: dict[Node, float], bicon_old: GraphAdj, bicon_new: GraphAdj, our_articulation_points: set[Node], articulation_subgraph_size: dict[Node, int]) -> dict[Node, float]:
    shortest_paths_old, preds_old, ordered_nodes_old = bfs_brandes(bicon_old, s) #* σ_s, P_s
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
            bc_upd[w] -= pair_dependency_old[w] / 2

        if (s in our_articulation_points):
            bc_upd[w] -= pair_dependency_old[w] * articulation_subgraph_size[s]
            bc_upd[w] -= external_dependency_old[w] / 2

    shortest_paths_new, preds_new, ordered_nodes_new = bfs_brandes(bicon_new, s) #* σ_s', P_s'
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
            bc_upd[w] += pair_dependency_new[w] / 2

        if (s in our_articulation_points):
            bc_upd[w] += pair_dependency_new[w] * articulation_subgraph_size[s]
            bc_upd[w] += external_dependency_new[w] / 2
    
    return bc_upd
