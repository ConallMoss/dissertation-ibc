from typing import Any
from networkx.classes.graph import Graph
from src.utils.my_imports import *
from src.utils.general import *
from src.utils.component_utils import *
from src.utils.dependency_utils import *

#* Modified for only single edge additions, to match iCentral
#* updates contains singular updating edge, and list of new nodes
#* Note: uses *edge* BCe not *node* BC
def LeeBCC(G: Graph, BCe: dict[Edge, float], e: Edge) -> dict[Edge, float]:
    v1, v2 = e

    V_ins: list[Node] = [] #* Check if either node is new to the graph
    #* Modified from paper to implicitly check for new nodes, instead of taking as arg
    for v in e:
        if v not in G.nodes:
            V_ins.append(v)

    #* Changed ordering to use graph before edge added
    G.add_nodes_from(V_ins)
    subgraphs: Optional[tuple[Graph, Graph]] = find_bridge_subgraphs(G, e)
    G.add_edge(v1, v2)

    #* Line 9: edge is a bridge between two subgraphs
    if (subgraphs):
        v_s, v_t = e 
        subgraph_s, subgraph_t = subgraphs
        #* Since we are only looking at edges within subgraph, can just use subgraph itself instead of full graph
        edge_pair_dependency_s: dict[Edge, float] = find_edge_pair_dependencies(subgraph_s, v_s) 
        edge_pair_dependency_t: dict[Edge, float] = find_edge_pair_dependencies(subgraph_t, v_t) 
        for e_s in subgraph_s.edges:
            #speed improvement on creating "norm" function
            BCe[(e_s if e_s[0] <= e_s[1] else (e_s[1], e_s[0]))] += len(subgraph_t) * edge_pair_dependency_s[e_s]
        for e_t in subgraph_t.edges:
            BCe[(e_t if e_t[0] <= e_t[1] else (e_t[1], e_t[0]))] += len(subgraph_s) * edge_pair_dependency_t[e_t]
        BCe[(e if e[0] <= e[1] else (e[1], e[0]))] = 1.0 * len(subgraph_s) * len(subgraph_t)

    #* Line 18:
    #* Since we only have one edge, is either bridge edge or not
    else:
        all_bicons: list[set[Any]] = find_biconnected_components(G)
        recalc_component: set[Any] = find_bicon_with_edge(all_bicons, e) #* Our bicon we are interested in
        print(f"recalculation size: {len(recalc_component)}")
        our_articulation_points: set[Any] = (find_articulation_points(G)).intersection(recalc_component)
        articulation_subgraph_size: dict[Node, int] = find_connected_subgraph_size(G, our_articulation_points, recalc_component)
        BCe_updated: dict[Edge, float] = edge_betweenness(G.subgraph(recalc_component).copy(), articulation_subgraph_size)
        BCe.update(BCe_updated)

    return BCe

#* Algorithm 2: UPDATE-BRANDES
def edge_betweenness(G: Graph, articulation_subgraph_sizes: dict[Node, int]) -> dict[Edge, float]:
    #* Brandes-style BC calculation, modified for BC on edges
    BCe_upd: dict[Edge, float] = defaultdict(float)
    articulation_points: set[Node] = set(articulation_subgraph_sizes.keys())
    G_adj: GraphAdj = G._adj
    for v_s in G.nodes:
        S: deque[Node] = deque() #Stack
        Q: deque[Node] = deque((v_s,)) #Queue
        P: dict[Node, list[Node]] = defaultdict(list) #empty set for each v in V
        σ: dict[Node, int] = defaultdict(int); σ[v_s] = 1
        d: dict[Node, int] = defaultdict(lambda: -1); d[v_s] = 0 #Use -1 for inf
        σ_t: dict[Node, int] = defaultdict(int) #No. type 2 SP for each v

        while Q:
            v_i: Node = Q.popleft()
            S.append(v_i)
            for v_n in G_adj[v_i]:
                if d[v_n] == -1:
                    Q.append(v_n)
                    d[v_n] = d[v_i] + 1
                if d[v_n] == d[v_i] + 1:
                    σ[v_n] += σ[v_i]
                    P[v_n].append(v_i)

        δ = defaultdict(float)  

        while S:
            v_n: Node = S.pop()
            if (v_s in articulation_points) and (v_n in articulation_points) and (v_n != v_s):
                #Add contribution from combined subgraph connections
                σ_t[v_n] += articulation_subgraph_sizes[v_s] * articulation_subgraph_sizes[v_n]

            for v_p in P[v_n]:
                δ[v_p] += σ[v_p]/σ[v_n] * (1 + δ[v_n])
                edge_increase: float = σ[v_p]/σ[v_n] * (1 + δ[v_n])
                if v_s in articulation_points:
                    #Increase for Type 2 SPs
                    σ_t[v_p] += σ_t[v_n] * σ[v_p] / σ[v_n] #type: ignore
                    #Add increase for Type 2 SPs
                    edge_increase += σ_t[v_p]
                    #Calc/add incr. for Type 1 SPs
                    edge_increase += articulation_subgraph_sizes[v_s] * σ[v_p] / σ[v_n] * (1 + δ[v_n]) * 2
                if edge_increase:
                    #speed improvement on creating norm function
                    #Halved as undirected graph
                    BCe_upd[(v_p, v_n) if v_p <= v_n else (v_n, v_p)] += edge_increase/2
    return BCe_upd