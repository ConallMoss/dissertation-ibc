d


def brandes(G: Graph) -> dict[Node, float]:
    BC: dict[Node, float] = defaultdict(float)
    for s in G.nodes: #Loop to find source dependency for every node
        #Setup variables required
        reverse_bfs_stack: Stack[Node] = Stack() #to store reverse BFS ordering
        preds: dict[Node, list] = defaultdict(list) #Predecessors of each node
        num_s_paths: dict[Node, int] = defaultdict(int)  #Number of shortest paths from s
        bfs_dist: dict[Node, int] = defaultdict(lambda: -1) #Distances
        bfs_queue: Queue[Node] = Queue([s]) #BFS queue
        source_dependency: dict[Node: float] = defaultdict(float) #Source dependencies
        σ[s] = 1; d[s] = 0 #Initialise source node values
        
        #Breadth-First Search
        while not Q.empty():
            v = Q.dequeue()
            S.push(v)
            for w in G: #G[v] represents the neighbours of v
                if d[w] < 0: #Node found for first time?
                    Q.enqueue(w)
                    d[w] = d[v] + 1
                if d[w] == d[v] + 1: #Exists shortest path to w via v?
                    σ[w] = σ[w] + σ[v]
                    P[w].append(v)
        
        #Reverse BFS order
        while not S.empty():
            w = S.pop()
            for v in P[w]:
                δ[v] = δ[v] + σ[v] / σ[w] * (1 + δ[w])
            if w != s:
                BC[w] = BC[w] + δ[w] #Add our source dependency to BC
    return BC