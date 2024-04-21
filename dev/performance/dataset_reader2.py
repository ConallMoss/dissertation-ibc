import networkx as nx

def get_dataset(name):
    return nx.read_edgelist(f"./datasets/{name}/out.{name}", nodetype=str, comments="%", data=False)

def get_lcc(G):
    return G.subgraph(max(nx.connected_components(G), key=len)).copy()

def get_bcc(G):
    return G.subgraph(max(nx.biconnected_components(G), key=len)).copy()

datasets = ("chess", "ego-facebook", "elec", "email-EuAll", "facebook-combined", "linux", "pajek-erdos", "slashdot-threads", "slashdot-zoo", "sx-mathoverflow", "topology", "wikispeedia")

for dataset in datasets:
    G = get_dataset(dataset)
    G_lcc = get_lcc(G)
    G_bcc = get_bcc(G)

    print(f"Graph: {dataset}")
    print(f"Nodes: {len(G.nodes):,}")
    print(f"Edges: {len(G.edges):,}")
    
    print("LCC:")
    print(f"Nodes: {len(G_lcc.nodes):,}")
    print(f"Edges: {len(G_lcc.edges):,}")
    
    print("BCC:")
    print(f"Nodes: {len(G_bcc.nodes):,}")
    print(f"Edges: {len(G_bcc.edges):,}")
    
    print(f"Diamteter: {nx.diameter(G_lcc)}")
    print("", flush=True)

    del G, G_lcc, G_bcc
