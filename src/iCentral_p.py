from src.utils.my_imports import *
from src.utils.general import *
from src.utils.bicon_utils import *
from src.utils.bfs_utils import *

from multiprocessing import Pool, Manager, get_logger

logger = logging.getLogger(__name__)

def iCentral_p(G: Graph, BC: dict[Node, float], e: Edge, PROCESSES=None) -> dict[Node, float]:
    logger.info("iCentral_p begun")
    v1, v2 = e
    G.add_edge(v1, v2)
    all_bicons = find_biconnected_components(G)
    all_articulation_points = find_articulation_points(G)

    #* We only care about the bicon with our new edge
    bicon_new = G.subgraph(find_bicon_with_edge(all_bicons, e)).copy() #* B_e'
    bicon_old = bicon_new.copy() #* B_e in paper
    bicon_old.remove_edge(v1, v2)

    our_articulation_points = all_articulation_points.intersection(bicon_new.nodes)
    articulation_subgraph_size = find_connected_subgraph_size(G, our_articulation_points, bicon_new.nodes)

    #* Line 4:
    d = {
        v1: bfs_distances(bicon_old, v1),
        v2: bfs_distances(bicon_old, v2)
    }

    #* Line 7:
    Q = deque() #Queue
    for s in bicon_old.nodes: 
        #* Check if ends of the edge are at different distances from edge endpoints
        #* i.e. if not, then edge would not be used
        if d[v1][s] != d[v2][s]: 
             Q.append(s)
    logger.info(f"{len(Q)=}")
    with Pool(processes=PROCESSES) as p, Manager() as manager:
        #* Required datastructures:
        #* bicon_old, bicon_new: Graph objects
        #* our_articulation_points: set of nodes
        #* articulation_subgraph_size: dict[node: int]
        bicon_old_manager = manager.dict(nx.to_dict_of_dicts(bicon_old))
        bicon_new_manager = manager.dict(nx.to_dict_of_dicts(bicon_new))
        #* manager does not support sets, only dicts 

        our_articulation_points_manager = manager.dict(dict.fromkeys(our_articulation_points, 0))
        articulation_subgraph_size_manager = manager.dict(dict.fromkeys(articulation_subgraph_size, 0))
        
        all_managers = (bicon_old_manager, bicon_new_manager, our_articulation_points_manager, articulation_subgraph_size_manager)
        no_managers = (bicon_old, bicon_new, our_articulation_points, articulation_subgraph_size)
        logger.info(f"multiprocessing calls: {PROCESSES=}")
        #* Multiprocessing calls to subfunctions
        bc_updates = p.starmap(calculate_node_dependencies_p, [(s, *no_managers) for s in Q])
        
        #* Add updates
        for bc_update in bc_updates:
            for k, v in bc_update.items():
                if v != 0:
                    BC[k] += v


def calculate_node_dependencies_p(s: Node, bicon_old, bicon_new, our_articulation_points, articulation_subgraph_size) -> dict[Node, float]:
    logger = get_logger()
    logger.info(f"Calc on {s}")
    BC_upd = defaultdict(float)

    shortest_paths_old, preds_old, ordered_nodes_old = bfs_brandes(bicon_old, s) #* σ_s, P_s
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
            BC_upd[w] -= pair_dependency_old[w] / 2

        if (s in our_articulation_points):
            BC_upd[w] -= pair_dependency_old[w] * articulation_subgraph_size[s]
            BC_upd[w] -= external_dependency_old[w] / 2

    shortest_paths_new, preds_new, ordered_nodes_new = bfs_brandes(bicon_new, s) #* σ_s', P_s'
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
            BC_upd[w] += pair_dependency_new[w] / 2

        if (s in our_articulation_points):
            BC_upd[w] += pair_dependency_new[w] * articulation_subgraph_size[s]
            BC_upd[w] += external_dependency_new[w] / 2
    logger.info(f"Calc on {s} complete")
    return BC_upd