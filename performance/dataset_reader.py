import networkx as nx
import time
import sys

def get_dataset(name):
    if name == "facebook_combined":
        return nx.read_edgelist(f"../datasets/facebook_combined.txt", nodetype=str , comments="%", data=False)
    return nx.read_edgelist(f"../datasets/{name}/out.{name}", nodetype=str, comments="%", data=False)

def get_lcc(G):
    return G.subgraph(max(nx.connected_components(G), key=len)).copy()

def get_bcc(G):
    return G.subgraph(max(nx.biconnected_components(G), key=len)).copy()

datasets = ["amazon-ratings", "chess", "com-dblp", "dimacs9-NY", "ego-facebook", "elec", "email-EuAll", "epinions", "facebook-wosn-links", "github", "linux", "munmun_twitter_social", "pajek-erdos", "slashdot-threads", "sx-mathoverflow", "web-NotreDame", "youtube-groupmemberships", "facebook_combined"]

for dataset in datasets:
    s = time.perf_counter()
    G = get_dataset(dataset)
    read_time = time.perf_counter() - s

    s = time.perf_counter()
    G_lcc = get_lcc(G)
    lcc_time = time.perf_counter() - s

    s = time.perf_counter()
    G_bcc = get_bcc(G)
    bcc_time = time.perf_counter() - s

    #edge_mem = sum([sys.getsizeof(e) for e in G.edges])
    #node_mem = sum([sys.getsizeof(n) for n in G.nodes])
    #G_mem = edge_mem + node_mem

    #edge_mem = sum([sys.getsizeof(e) for e in G_lcc.edges])
    #node_mem = sum([sys.getsizeof(n) for n in G_lcc.nodes])
    #G_mem_lcc = edge_mem + node_mem

    #edge_mem = sum([sys.getsizeof(e) for e in G_bcc.edges])
    #node_mem = sum([sys.getsizeof(n) for n in G_bcc.nodes])
    #G_mem_bcc = edge_mem + node_mem


    print(f"Graph: {dataset}")
    print(f"Nodes: {len(G.nodes):,}")
    print(f"Edges: {len(G.edges):,}")
    #print(f"Readtime: {read_time}")
    #print(f"Memory: {G_mem:,}")
    print("LCC:")
    print(f"Nodes: {len(G_lcc.nodes):,}")
    print(f"Edges: {len(G_lcc.edges):,}")
    #print(f"Readtime: {lcc_time}")
    #print(f"Memory: {G_mem_lcc:,}")
    print("BCC:")
    print(f"Nodes: {len(G_bcc.nodes):,}")
    print(f"Edges: {len(G_bcc.edges):,}")
    #print(f"Readtime: {bcc_time}")
    #print(f"Memory: {G_mem_bcc:,}")
    print("")

    del G, G_lcc, G_bcc


    
    
