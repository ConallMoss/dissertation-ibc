import networkx as nx

def get_dataset(name):
    return nx.read_edgelist(f"./datasets/{name}/out.{name}", nodetype=str, comments="%", data=False)

def get_lcc(G):
    G2 = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    G2.remove_edges_from(nx.selfloop_edges(G2))
    return G2

def get_bcc(G):
    return G.subgraph(max(nx.biconnected_components(G), key=len)).copy()

datasets = ("email-EuAll", "linux", "topology", "sx-mathoverflow", "slashdot-threads", "chess",  "elec",  "facebook-combined", "wikispeedia", "pajek-erdos")

for dataset in datasets:
    G = get_dataset(dataset)
    G_lcc = get_lcc(G)
    G_bcc = get_bcc(G_lcc)

    print(f"Graph: {dataset}")
    print(f"Nodes: {len(G.nodes):,}")
    print(f"Edges: {len(G.edges):,}")
    
    print("LCC:")
    print(f"Nodes: {len(G_lcc.nodes):,}")
    print(f"Edges: {len(G_lcc.edges):,}")
    
    print("BCC:")
    print(f"Nodes: {len(G_bcc.nodes):,}")
    print(f"Edges: {len(G_bcc.edges):,}")

    print("Nodes BCC/LCC")
    print(len(G_bcc.nodes)/len(G_lcc.nodes))

    print("Average vertex degree")
    print(len(G.edges)/len(G.nodes)*2)
    
    #print(f"Diamteter: {nx.diameter(G_lcc)}")
    print("", flush=True)

    del G, G_lcc, G_bcc
