from multiprocessing.managers import DictProxy
from multiprocessing.synchronize import Lock as LockBase
from typing import Any
from src.utils.my_imports import *
from src.utils.general import *
from src.utils.component_utils import *
from src.utils.bfs_utils import *

from multiprocessing import Pool, Manager, get_logger, Process, Queue, Lock
from multiprocessing.managers import DictProxy
from multiprocessing.synchronize import Lock as LockBase
import multiprocessing

logger = logging.getLogger(__name__)

def iCentral_p(G: Graph, BC: dict[Node, float], e: Edge, PROCESSES: int=20) -> dict[Node, float]:
    if PROCESSES is None:
        PROCESSES = multiprocessing.cpu_count()

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
    d1 = bfs_distances(bicon_old, v1)
    d2 = bfs_distances(bicon_old, v2)

    #* Line 7:
    #* Using threadsafe multi-processing queue
    Q: Queue = Queue() #Queue
    for s in bicon_old.nodes: 
        #* Check if ends of the edge are at different distances from edge endpoints
        #* i.e. if not, then edge would not be used
        if d1[s] != d2[s]: 
             Q.put(s)

    #* Undefault the dict - used for testing when a default dict is passed in
    for n in G.nodes:
        if n not in BC:
            BC[n] = 0
    #* Thread safe dictionary update manager
    with Manager() as manager:
        #* Setup inputs for each call

        #bicon_old_manager = manager.dict(nx.to_dict_of_dicts(bicon_old))
        #bicon_new_manager = manager.dict(nx.to_dict_of_dicts(bicon_new))
        #our_articulation_points_manager = manager.dict(dict.fromkeys(our_articulation_points, 0))
        #articulation_subgraph_size_manager = manager.dict(dict.fromkeys(articulation_subgraph_size, 0))

        bicon_old_adj: GraphAdj = bicon_old._adj
        bicon_new_adj: GraphAdj = bicon_new._adj

        resources: tuple = (bicon_old_adj, bicon_new_adj, our_articulation_points, articulation_subgraph_size)
        bc_manager: DictProxy[Node, float] = manager.dict(BC)
        manager_lock: LockBase = Lock()
        all_processes: list[Process] = []

        #* Spawn all processes
        for _ in range(PROCESSES):
            p: Process = Process(target=run, args=(Q, bc_manager, manager_lock, resources))
            p.start()
            all_processes.append(p)

        #* Wait for all processes to complete
        for p in all_processes:
            p.join()

        BC = dict(bc_manager)

    # #* Redefault the dict
    # for k, v in list(BC.items()):
    #     if v == 0:
    #         del BC[k]

    return BC
 

def run(q: Queue, bc_manager: DictProxy, manager_lock: LockBase, resources: tuple):
        while not q.empty():
            s: Node = q.get()
            bc_upd: dict[Node, float] = calculate_node_dependencies_p(s, *resources)
            with manager_lock:
                for k, v in bc_upd.items():
                    if v != 0:
                        bc_manager[k] += v

def calculate_node_dependencies_p(s: Node, bicon_old: GraphAdj, bicon_new: GraphAdj, our_articulation_points: set[Node], articulation_subgraph_size: dict[Node, int]) -> dict[Node, float]:
    BC_upd = defaultdict(float)

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
            BC_upd[w] -= pair_dependency_old[w] / 2

        if (s in our_articulation_points):
            BC_upd[w] -= pair_dependency_old[w] * articulation_subgraph_size[s]
            BC_upd[w] -= external_dependency_old[w] / 2

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
            BC_upd[w] += pair_dependency_new[w] / 2

        if (s in our_articulation_points):
            BC_upd[w] += pair_dependency_new[w] * articulation_subgraph_size[s]
            BC_upd[w] += external_dependency_new[w] / 2
    
    return BC_upd
