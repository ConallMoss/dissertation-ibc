from src.utils.my_imports import *

Graph = nx.Graph
Node =  Any #* Type Alias
Edge = tuple[Node, Node] #* Faster than dataclass or other forms
GraphAdj = dict[Node, set[Node]] #* Same behaviour as graph for neighbor getting
