from tests.testing_utils import *
from pytest import approx
from src.utils.bfs_utils import *

def test_bfs_brandes_basic():
    """
    Test Brandes BFS on basic small graph
    """
    #* Arrange
    G = nx.Graph([(0,1), (1,2), (2,3), (0,3), (3,4)])
    s = 1

    expected_sigma = {1: 1, 0: 1, 2: 1, 3: 2, 4: 2}
    expected_parents = {0: [1], 2: [1], 3: [0, 2], 4: [3]}
    expected_order = [4, 3, 2, 0, 1]

    #* Act
    sigma, parents, order = bfs_brandes(G, s)

    #* Assert
    assert dict(sigma) == expected_sigma
    assert dict(parents) == expected_parents
    assert list(order) == expected_order

def test_bfs_brandes_larger():
    """
    Test Brandes BFS on larger graph
    """
    #* Arrange
    G = nx.Graph([(1,2), (1, 4), (2, 3), (3, 4), (3, 5), (3, 8), (4, 6), (5, 8), (6,7), (7,8)])
    s = 4

    expected_sigma = {4: 1, 1: 1, 3: 1, 6: 1, 2: 2, 5: 1, 8: 1, 7: 1}
    expected_parents = {1: [4], 3: [4], 6: [4], 2: [1, 3], 5: [3], 8: [3], 7: [6]}
    expected_order = [7, 8, 5, 2, 6, 3, 1, 4]

    #* Act
    sigma, parents, order = bfs_brandes(G, s)

    #* Assert
    assert dict(sigma) == expected_sigma
    assert dict(parents) == expected_parents
    assert list(order) == expected_order

def test_bfs_distances_basic():
    """
    Test BFS distances on basic small graph
    """
    #* Arrange
    G = nx.Graph([(0,1), (1,2), (2,3), (0,3), (3,4)])
    s = 1

    expected_distance = {1: 0, 0: 1, 2: 1, 3: 2, 4: 3}

    #* Act
    distance = bfs_distances(G, s)

    #* Assert
    assert dict(distance) == expected_distance

def test_bfs_distances_larger():
    """
    Test BFS distances on larger graph
    """
    #* Arrange
    G = nx.Graph([(1,2), (1, 4), (2, 3), (3, 4), (3, 5), (3, 8), (4, 6), (5, 8), (6,7), (7,8)])
    s = 4

    expected_distance = {4: 0, 1: 1, 3: 1, 6: 1, 2: 2, 5: 2, 8: 2, 7: 2}

    #* Act
    distance = bfs_distances(G, s)

    #* Assert
    assert dict(distance) == expected_distance