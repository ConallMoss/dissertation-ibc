from src.utils.my_imports import *
from src.utils.general import *
from src.utils.bicon_utils import *
from src.utils.leebcc_utils import *

#* Modified for only single edge additions, to match iCentral
#* updates contains singular updating edge, and list of new nodes
#* Note: uses *edge* BCe not *node* BC
def LeeBCC(G: Graph, BCe: dict[Edge, float], e: Edge, V_ins: list[Node] = None) -> dict[Edge, float]:
    if V_ins is None:
        V_ins = []
    v1, v2 = e

    #* Changed ordering to use graph before edge added
    subgraphs = find_bridge_subgraphs(G, e)
    G.add_edge(v1, v2)
    G.add_nodes_from(V_ins)

    #* Line 4:
    for v in V_ins:
        edge_pair_dependency = find_edge_pair_dependencies(G, v)
        for e in G.edges:
            BCe[e] += edge_pair_dependency[e]

    #* Line 9:
    if (subgraphs):
        v_s, v_t = e 
        subgraph_s, subgraph_t = subgraphs
        #* Since we are only looking at edges within subgraph, can just use subgraph itself instead of full graph
        edge_pair_dependency_s = find_edge_pair_dependencies(subgraph_s, v_s) 
        edge_pair_dependency_t = find_edge_pair_dependencies(subgraph_t, v_t) 
        for e in subgraph_s.edges:
            #speed improvement on creating "norm" function
            BCe[(e if e[0] <= e[1] else (e[1], e[0]))] += len(subgraph_t) * edge_pair_dependency_s[e]
        for e in subgraph_t.edges:
            BCe[(e if e[0] <= e[1] else (e[1], e[0]))] += len(subgraph_s) * edge_pair_dependency_t[e]

    #* Line 18:
    #* Since we only have one edge, is either bridge edge or not
    else:
        all_bicons = find_biconnected_components(G)
        recalc_component = find_bicon_with_edge(all_bicons, e) #* Our bicon we are interested in
        our_articulation_points = (find_articulation_points(G)).intersection(recalc_component)
        articulation_subgraph_size = find_connected_subgraph_size(G, our_articulation_points, recalc_component)
        BCe_updated = edge_betweenness(G.subgraph(recalc_component).copy(), articulation_subgraph_size)
        BCe.update(BCe_updated)

    return BCe

#* Algorithm 2: UPDATE-BRANDES
def edge_betweenness(G: Graph, articulation_subgraph_sizes: dict[Node, int]) -> dict[Edge, float]:
    #* Brandes-style BC calculation, modified for BC on edges
    BCe_upd = defaultdict(float)
    articulation_points = set(articulation_subgraph_sizes.keys())
    G_adj = G._adj
    for v_s in G.nodes:
        S = deque() #Stack
        Q = deque((v_s,)) #Queue
        P = defaultdict(list) #empty set for each v in V
        σ = defaultdict(int); σ[v_s] = 1
        d = defaultdict(lambda: -1); d[v_s] = 0 #Use -1 for inf
        σ_t = defaultdict(int) #No. type 2 SP for each v

        while Q:
            v_i = Q.popleft()
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
            v_n = S.pop()
            if (v_s in articulation_points) and (v_n in articulation_points) and (v_n != v_s):
                #Add contribution from combined subgraph connections
                σ_t[v_n] += articulation_subgraph_sizes[v_s] * articulation_subgraph_sizes[v_n]

            for v_p in P[v_n]:
                δ[v_p] += σ[v_p]/σ[v_n] * (1 + δ[v_n])
                edge_increase = σ[v_p]/σ[v_n] * (1 + δ[v_n])
                if v_s in articulation_points:
                    #Increase for Type 2 SPs
                    σ_t[v_p] += σ_t[v_n] * σ[v_p] / σ[v_n]
                    #Add increase for Type 2 SPs
                    edge_increase += σ_t[v_n] * σ[v_p] / σ[v_n]
                    #Calc/add incr. for Type 1 SPs
                    edge_increase += articulation_subgraph_sizes[v_s] * σ[v_p] / σ[v_n] * (1 + δ[v_n]) * 2
                if edge_increase:
                    #speed improvement on creating norm function
                    #Halved as undirected graph
                    BCe_upd[(v_p, v_n) if v_p <= v_n else (v_n, v_p)] += edge_increase/2
    return BCe_upd