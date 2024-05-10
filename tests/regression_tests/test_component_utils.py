from tests.testing_utils import *
from pytest import approx
from src.utils.component_utils import *

def test_find_connected_subgraph_size():
    """
    Test find connected subgraph size on biconnected graph.
    """
    #* Arrange
    G = nx.Graph({
        9: [10, 11],
        10: [9,11,1],
        11: [9, 1],
        1: [2, 4, 10, 11],
        13: [12, 14],
        12: [13, 6],
        14: [13, 6],
        6: [4, 7],
        7:[6, 8],
        8: [5, 7],
        4: [1,2,6],
        2:[1,4],
        3: [4,5],
        5: [15,19,3,8],
        15: [5,17],
        19:[5, 17],
        17: [15, 19, 16, 20],
        16: [17, 18],
        20: [17, 18],
        18: [16, 20]
    })
    our_ap = {4, 5, 6}
    our_bicon = {5, 8, 7, 6, 4, 3}

    expected_subgraph_sizes = {4: 5, 5: 6, 6: 3}

    #* Act
    subgraph_sizes = find_connected_subgraph_size(G, our_ap, our_bicon)

    #* Assert
    assert subgraph_sizes == expected_subgraph_sizes