import networkx as nx
from typing import Any

Graph = nx.Graph
Node =  Any #* Type Alias
Edge = tuple[Node, Node] #* Faster than dataclass or other forms
GraphAdj = dict[Node, set[Node]] #* Same behaviour as graph for neighbor getting
