# %%
import networkx as nx
import random
import matplotlib.pyplot as plt
from dataclasses import dataclass, field
from typing import List, Any, Tuple, Dict

# %%
Graph = nx.Graph
Node = Any
Edge = Tuple[Node, Node]

# %%
#* Utility Functions
def norm_edge(v1, v2):
    return (v1, v2) if v1 <= v2 else (v2, v1)

def loss_fn(v1: float, v2: float) -> float: #? rename to "difference"
    """Loss function to use between two values"""
    #return (v1-v2)**2 #* Alternative loss func
    return abs(v1-v2)

def get_dict_loss(d1: Dict[Node, float], d2: Dict[Node, float]) -> float:
    """Get sum of losses across two dicts (dict default 0 if not found)"""
    loss = 0.0
    keys = set(d1.keys()).union(set(d2.keys()))
    for k in keys:
        loss += loss_fn(d1.get(k, 0), d2.get(k, 0)) 
    return loss

def get_bc(G: Graph) -> dict[Node, float]:
    bc = dict(nx.betweenness_centrality(G, normalized=False))
    edge_count = G.number_of_edges() 
    if edge_count == 0:
        return bc
    for k, v in bc.items():
        bc[k] = v / edge_count
    return bc

def get_loss_info(G: Graph, edgelist: List[Edge]) -> dict:
    final_bc = get_bc(G)
    G2 = Graph() 

    #* Tracked values:
    losses = []
    num_cc = []
    num_nodes = []
    num_bicons = []

    #* Add initial defaults
    losses.append(get_dict_loss(get_bc(G2), final_bc))
    num_cc.append(1) 
    num_nodes.append(0)
    num_bicons.append(1)
    
    #* Iterate through edges:
    for e in edgelist:
        if e in G2.edges:
            continue #* Protect against re-adding an edge
        G2.add_edge(*e)
        losses.append(get_dict_loss(get_bc(G2), final_bc))
        num_cc.append(nx.number_connected_components(G2) or 1) 
        num_nodes.append(G2.number_of_nodes())
        num_bicons.append(len(list(nx.biconnected_components(G2))) or 1)

    loss_info = {
        "losses": losses,
        "num_cc": num_cc,
        "num_nodes": num_nodes,
        "num_bicons": num_bicons,
    }

    return loss_info

# %%
#* Plot funcs
def double_plot(loss_info: dict, property: str, name=None):
    fig, ax1 = plt.subplots()

    ax2 = ax1.twinx()

    cols = {
        "losses": "red",
        "num_cc": "green",
        "num_nodes": "orange",
        "num_bicons": "blue",
        "all": "black",
    }

    names = {
        "num_bicons": "Number of biconnected components",
        "num_cc": "Number of connected components",
        "num_nodes": "Number of nodes",
        "all": "All"
    }

    ax1.plot(loss_info["losses"], color=cols["losses"], label="losses")
    if property == "all":
        for prop in ["num_cc", "num_nodes", "num_bicons"]:
            ax2.plot(loss_info[prop], color=cols[prop], label=prop)
    else:
        ax2.plot(loss_info[property], color=cols[property], label=property)

    ax1.set_ylabel("Loss Metric", color=cols["losses"])
    ax2.set_ylabel(names[property], color=cols[property])
    ax1.set_xlabel("Number of edges inserted from edgelist")
    
    #fig.legend(["Loss", names[property]], loc=2)
    fig.tight_layout()
    if name:
        plt.savefig(f'figs/{name}.pdf', dpi=300)
    plt.show()

# %%
#* Edgelist functions

#* Edge removal helper func
def get_edge_remove_loss(G, e, true_bc):
        G.remove_edge(e[0], e[1])
        l = get_dict_loss(get_bc(G), true_bc)
        G.add_edge(e[0], e[1])
        return l

#* Edge addition helper func
def get_edge_add_loss(G, e, true_bc):
        G.add_edge(e[0], e[1])
        l = get_dict_loss(get_bc(G), true_bc)
        G.remove_edge(e[0], e[1])
        return l

def get_greedy_backward_edgelist(G, G_base=None, min_loss=True):
    """Get edgelist where edges chosen by least change to loss across options, working backward"""
    if G_base is None:
        base = nx.Graph()
    else:
        base = G_base.copy()
    main = G.copy()
    max_or_min = min if min_loss else max
    true_bc = get_bc(G)
    all_edges = set(G.edges) - set(base.edges)

    edge_order = []
    while all_edges:
        best_edge = max_or_min(all_edges, key=lambda e: get_edge_remove_loss(main, e, true_bc))
        edge_order.append(best_edge)
        main.remove_edge(best_edge[0], best_edge[1])
        all_edges.remove(best_edge)
    return edge_order[::-1]

def get_greedy_forward_edgelist(G, G_base=None, min_loss=True):
    """Get edgelist where edges chosen by least change to loss across all options"""
    if G_base is None:
        base = nx.Graph()
    else:
        base = G_base.copy()
    max_or_min = min if min_loss else max
    true_bc = get_bc(G)
    all_edges = set(G.edges) - set(base.edges)
    edge_order = []
    while all_edges:
        best_edge = max_or_min(all_edges, key=lambda e: get_edge_add_loss(base, e, true_bc))
        edge_order.append(best_edge)
        base.add_edge(best_edge[0], best_edge[1])
        all_edges.remove(best_edge)
    return edge_order

#* BCE ordered edgelist
def get_bce_edgelist(G, good=True):
    bce = nx.edge_betweenness_centrality(G)
    return [k for k, _ in sorted(bce.items(), key=lambda item: item[1], reverse=good)]

#* DC ordered edgelist
def get_dc_edgelist(G, good=True):
    dc = nx.degree_centrality(G)
    dc_nodes_order = [k for k, _ in sorted(dc.items(), key=lambda item: item[1], reverse=good)]
    edgelist = []
    seen_edges = set()
    for node in dc_nodes_order:
        ordered_neighbours = sorted(list(G[node]), key=dc_nodes_order.index)
        for neighbour in ordered_neighbours:
            if (node, neighbour) not in seen_edges:
                seen_edges.add((node, neighbour))
                seen_edges.add((neighbour, node))
                edgelist.append((node, neighbour))
    return edgelist

# %%
#* Other edgelists
#* Randomised edgelist
def get_random_edgelist(G):
    G_edges = list(G.edges)
    return random.sample(G_edges, len(G_edges))

def get_random_dc_weighted_node(G):
    dc = nx.degree_centrality(G)
    dc_keys = list(dc.keys())
    dc_weights = list(dc.values())
    return random.choices(list(dc.keys()), weights=list(dc.values()))[0]

#* BFS, source chosen weighted by dc
def get_bfs_edgelist(G, source=None):
    if source is None:
        source = get_random_dc_weighted_node(G)
    return list(nx.edge_bfs(G, source))

#* DFS, source chosen weighted by dc
def get_dfs_edgelist(G, source=None):
    if source is None:
        source = get_random_dc_weighted_node(G)
    return list(nx.edge_dfs(G, source))

#* Explore from frontier of available edges, nodes chosen by choice
def get_frontier_explore_edgelist(G, source=None, choice="dc"):
    edgelist = []
    if source is None:
        source = get_random_dc_weighted_node(G)
    if choice == "dc":
        dc = nx.degree_centrality(G)
        dc_nodes_order = [i for i, _ in sorted(dc.items(), key=lambda item: item[1], reverse=True)]
        def pick(nodes):
            return min(nodes, key=dc_nodes_order.index)
    else:
        def pick(nodes):
            return random.choice(nodes)
    frontier = [source]
    seen = set()
    while frontier:
        node = pick(frontier)
        frontier.remove(node)
        seen.add(node)
        for neighbour in G[node]:
            if neighbour not in seen:
                frontier.append(neighbour)
                edgelist.append((node, neighbour))

    return edgelist


# %%
#* Actual testing

G = nx.karate_club_graph()
#G = nx.les_miserables_graph()
G_base = nx.Graph()
G_edges = list((G.edges))
random.seed(42)
# %%
rand_runs = 10

edgelist_greedy_forward = get_greedy_forward_edgelist(G)
edgelist_greedy_backward = get_greedy_backward_edgelist(G)
edgelist_greedy_forward_adv = get_greedy_forward_edgelist(G, min_loss=False)
edgelist_greedy_backward_adv = get_greedy_backward_edgelist(G, min_loss=False)

edgelist_bce_good = get_bce_edgelist(G)
edgelist_bce_bad = get_bce_edgelist(G, good=False)

edgelist_dc_good = get_dc_edgelist(G)
edgelist_dc_bad = get_dc_edgelist(G, good=False)

edgelist_bfs = get_bfs_edgelist(G)
edgelist_dfs = get_dfs_edgelist(G)

edgelists_random = [get_random_edgelist(G) for _ in range(rand_runs)]

edgelists_frontier_random = [get_frontier_explore_edgelist(G, choice="random") for _ in range(rand_runs)]
edgelists_frontier_dc = [get_frontier_explore_edgelist(G, choice="dc") for _ in range(rand_runs)]
# %%
loss_info_greedy_forward = get_loss_info(G, edgelist_greedy_forward)
loss_info_greedy_backward = get_loss_info(G, edgelist_greedy_backward)
loss_info_greedy_forward_adv = get_loss_info(G, edgelist_greedy_forward_adv)
loss_info_greedy_backward_adv = get_loss_info(G, edgelist_greedy_backward_adv)

loss_info_bce_good = get_loss_info(G, edgelist_bce_good)
loss_info_bce_bad = get_loss_info(G, edgelist_bce_bad)

loss_info_dc_good = get_loss_info(G, edgelist_dc_good)
loss_info_dc_bad = get_loss_info(G, edgelist_dc_bad)

loss_info_bfs = get_loss_info(G, edgelist_bfs)
loss_info_dfs = get_loss_info(G, edgelist_dfs)

losses_info_random = [get_loss_info(G, edgelist) for edgelist in edgelists_random]

losses_info_frontier_random = [get_loss_info(G, edgelist) for edgelist in edgelists_frontier_random]
losses_info_frontier_dc = [get_loss_info(G, edgelist) for edgelist in edgelists_frontier_dc]

# %%
# %%

plt.plot(loss_info_greedy_backward["losses"])
plt.plot(loss_info_greedy_forward["losses"])
plt.legend(["Backward", "Forward"])
plt.xlabel("Edge insertions")
plt.ylabel("Distance metric")
#plt.title("Performance of ")

# %%
# %%
plt.plot(loss_info_bce_good["losses"])
plt.plot(loss_info_bce_bad["losses"])
plt.plot(loss_info_dc_good["losses"])
plt.plot(loss_info_dc_bad["losses"])
plt.legend(["bce good", "bce bad", "dc good", "dc bad"])
# %%
double_plot(loss_info_dc_good, "num_bicons")
double_plot(loss_info_dc_good, "num_cc")
double_plot(loss_info_dc_good, "num_nodes")
# %%
double_plot(loss_info_bce_good, "num_bicons")
double_plot(loss_info_bce_good, "num_cc")
double_plot(loss_info_bce_good, "num_nodes")
# %%
double_plot(loss_info_greedy_backward, "all")
# %%
double_plot(loss_info_greedy_forward, "all")
# %%
double_plot(loss_info_greedy_backward_adv, "all")
# %%
double_plot(loss_info_greedy_forward_adv, "all")
# %%
double_plot(loss_info_bfs, "all")
# %%
double_plot(loss_info_dfs, "all")
# %%
double_plot(losses_info_random[1], "all")
# %%
double_plot(losses_info_frontier_dc[0], "all")
# %%
double_plot(losses_info_frontier_random[1], "all")
# %%
double_plot(losses_info_frontier_dc[0], "all")

# %%

#* Direct comparisons:

# %%
#* General comparison
plt.plot(loss_info_bce_good["losses"])
plt.plot(loss_info_dc_good["losses"])
plt.plot(loss_info_greedy_backward["losses"])
plt.plot(loss_info_greedy_forward["losses"])
plt.plot(losses_info_random[1]["losses"])
plt.plot(losses_info_frontier_random[1]["losses"])
plt.plot(losses_info_frontier_dc[1]["losses"])

plt.legend(["bce", "dc", "backward", "forward",  "random", "random exp", "dc exp"])
# %%
#* bit of a mess
# plt.plot(losses_random_avg)
# for losses in losses_info_random:
#     plt.plot(losses["losses"])
# plt.legend(["avg"])
# %%
#* Comparison of how quickly nodes are added
plt.plot(loss_info_bce_good["num_nodes"])
plt.plot(loss_info_dc_good["num_nodes"])
plt.plot(loss_info_greedy_backward["num_nodes"])
plt.plot(loss_info_greedy_forward["num_nodes"])
plt.plot(losses_info_random[9]["num_nodes"])
plt.legend(["bce", "dc", "forward", "backward"])


#%%
fig, axs = plt.subplots(2, 2)
fig.suptitle("Loss of edge ordering over insertions")
axs[0, 0].plot(loss_info_greedy_backward["losses"])
axs[0, 0].plot(loss_info_greedy_forward["losses"])
axs[0, 0].legend(["Backward", "Forward"], fontsize="8")

for ax in axs.flat:
    ax.set(xlabel='Edge Insertions', ylabel='Loss')

for ax in axs.flat:
    ax.label_outer()
# %%

# !!!!!
plt.plot(loss_info_greedy_backward["losses"], "tab:blue")
plt.plot(loss_info_greedy_forward["losses"], "tab:orange")
plt.plot(loss_info_bce_good["losses"], "tab:red")
plt.plot(loss_info_dc_good["losses"], "tab:green")
plt.legend(["Backward", "Forward", "Betweenness", "Degree"])
plt.xlabel("Number of edges inserted from edgelist")
plt.ylabel("Loss metric")

plt.tight_layout()
plt.savefig('figs/ext_edgelists1.pdf', dpi=300)
plt.show()

# %%
plt.plot(loss_info_bce_good["losses"])
plt.plot(loss_info_dc_good["losses"])
plt.plot(loss_info_greedy_backward["losses"])
plt.legend(["Betweenness", "Degree", "Backward"])
plt.xlabel("Edge insertions")
plt.ylabel("Loss metric")



# %%
plt.plot(loss_info_bfs["losses"], "tab:cyan")
plt.plot(loss_info_dfs["losses"], "tab:purple")
plt.plot(loss_info_bce_good["losses"], "tab:red")
plt.plot(loss_info_greedy_backward["losses"], "tab:green")
plt.legend(["BFS", "DFS", "Betweenness", "Backward"])
plt.xlabel("Number of edges inserted from edgelist")
plt.ylabel("Loss metric")

plt.tight_layout()
plt.savefig('figs/ext_edgelists2.pdf', dpi=300)
plt.show()
# %%
plt.plot(losses_info_random[1]["losses"])
plt.plot(losses_info_frontier_random[1]["losses"])
plt.plot(loss_info_greedy_backward["losses"])
plt.legend(["Random", "Random Fronteir", "Backward"])
plt.xlabel("Edge insertions")
plt.ylabel("Loss metric")
# %%

double_plot(loss_info_dc_good, "num_bicons")

# %%
double_plot(loss_info_bce_good, "num_bicons")

# %%
double_plot(loss_info_greedy_backward, "num_bicons")
# %%
double_plot(loss_info_greedy_forward, "num_bicons")
# %%
double_plot(loss_info_bfs, "num_bicons")
# %%
double_plot(loss_info_dfs, "num_bicons")
# %%
double_plot(loss_info_bce_good, "num_bicons")
double_plot(loss_info_bce_good, "num_nodes")
double_plot(loss_info_bce_good, "num_cc")
# %%

double_plot(loss_info_bce_good, "num_bicons", name="ext_bce_bicons")

# %%
double_plot(loss_info_bce_good, "num_cc", name="ext_bce_cc")
# %%
double_plot(loss_info_bce_good, "num_nodes", name="ext_bce_nodes")
# %%
