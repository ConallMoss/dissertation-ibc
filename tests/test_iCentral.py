
from tests.testing_utils import *
from pytest import approx

def test_iCentral_basic():
    """
    Test iCentral on: Basic 4 node square
    """
    #* Arrange
    G = nx.Graph()
    G.add_edges_from([(2,3), (3,4), (1,2)])
    e = (1,4)
    
    #* Act
    bc_new, bc_iCentral = dotest_iCentral(G, e)

    #* Assert
    assert bc_new == approx(bc_iCentral)

def test_iCentral_from_paper():
    """
    Test iCentral on: Example BC Graph from paper (pg_)
    """
    #* Arrange
    G = nx.Graph()
    G.add_edges_from([(1,2), (1, 4), (2, 3), (3, 4), (3, 5), (3, 8), (4, 6), (5, 8), (6,7), (7,8)])
    e = (4,8)
    
    #* Act
    bc_new, bc_iCentral = dotest_iCentral(G, e)

    #* Assert
    assert bc_new == approx(bc_iCentral)

def test_iCentral_many_components():
    """
    Test iCentral on: Example Biconnected Components Graph from paper (pg_)
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
    4: [1,3,6],
    2:[1,3],
    3: [2,4,5],
    5: [15,19,3,8],
    15: [5,17],
    19:[5, 17],
    17: [15, 19, 16, 20],
    16: [17, 18],
    20: [17, 18],
    18: [16, 20]
    })
    e = (4,8)
    #* Act
    bc_new, bc_iCentral = dotest_iCentral(G, e)

    #* Assert
    assert bc_new == approx(bc_iCentral)

def test_iCentral_pregen():
    """
    Test iCentral on: Generated graph 1
    """
    #* Arrange
    G = nx.Graph({
        0: {7: {}},
        1: {10: {}},
        2: {13: {}, 14: {}},
        3: {6: {}, 9: {}},
        4: {11: {}, 14: {}},
        5: {12: {}},
        6: {3: {}, 8: {}},
        7: {0: {}, 10: {}, 12: {}},
        8: {6: {}, 9: {}},
        9: {3: {}, 8: {}, 10: {}, 11: {}},
        10: {1: {}, 7: {}, 9: {}},
        11: {4: {}, 9: {}, 13: {}},
        12: {5: {}, 7: {}, 13: {}},
        13: {2: {}, 11: {}, 12: {}},
        14: {2: {}, 4: {}}
    })
    e = (3,4)
    
    #* Act
    bc_new, bc_iCentral = dotest_iCentral(G, e)

    #* Assert
    assert bc_new == approx(bc_iCentral)

def test_iCentral_randEdge_nxsocial_karate():
    """
    Test iCentral on: nx social: karate club graph, with randomly generated insert edge
    """
    #* Arrange
    G = nx.karate_club_graph()
    e = pick_random_nonedge(G, seed=42)
    
    #* Act
    bc_new, bc_iCentral = dotest_iCentral(G, e)
    print(bc_iCentral)

    #* Assert
    assert bc_new == approx(bc_iCentral)

#* Repeat for other social graphs
    
def test_iCentral_randEdge_ER256():
    """
    Test iCentral on: Erdos-Reyni (n=256, p=0.5) graph, with randomly generated insert edge
    """
    #* Arrange
    G =  nx.erdos_renyi_graph(256, 0.5, seed=123, directed=False)
    e = pick_random_nonedge(G, seed=42)
    
    #* Act
    bc_new, bc_iCentral = dotest_iCentral(G, e)
    print(bc_iCentral)

    #* Assert
    assert bc_new == approx(bc_iCentral)

# def test_iCentral_randEdge_ER1024():
#     """
#     Test iCentral on: Erdos-Reyni (n=1024, p=1/32) graph, with randomly generated insert edge
#     """
#     #* Arrange
#     G =  nx.erdos_renyi_graph(1024, 1/32, seed=123, directed=False)
#     e = pick_random_nonedge(G, seed=42)
    
#     #* Act
#     bc_new, bc_iCentral = dotest_iCentral(G, e)
#     print(bc_iCentral)

#     #* Assert
#     assert bc_new == approx(bc_iCentral)