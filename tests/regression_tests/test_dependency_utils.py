from tests.testing_utils import *
from pytest import approx
from src.utils.dependency_utils import *

def test_edge_source_dependencies_basic():
    """
    Test edge source dependencies on basic small graph
    """
    #* Arrange
    G = nx.Graph([(0,1), (1,2), (2,3), (0,3), (3,4)])
    s = 1

    expected_edge_dep = {(3, 4): 1.0, (0, 3): 1.0, (2, 3): 1.0, (1, 2): 2.0, (0, 1): 2.0}

    #* Act
    edge_dep = find_edge_source_dependencies(G, s)

    #* Assert
    assert dict(edge_dep) == approx(expected_edge_dep)

def test_edge_source_dependencies_larger():
    """
    Test edge source dependencies on larger graph
    """
    #* Arrange
    G = nx.Graph([(1,2), (1, 4), (2, 3), (3, 4), (3, 5), (3, 8), (4, 6), (5, 8), (6,7), (7,8)])
    s = 4

    expected_edge_dep = {(6, 7): 1.0,
             (3, 8): 1.0,
             (3, 5): 1.0,
             (1, 2): 0.5,
             (2, 3): 0.5,
             (4, 6): 2.0,
             (3, 4): 3.5,
             (1, 4): 1.5}

    #* Act
    edge_dep = find_edge_source_dependencies(G, s)

    #* Assert
    assert dict(edge_dep) == approx(expected_edge_dep)

def test_node_pair_dependencies_basic():
    """
    Test node pair dependencies on basic small graph
    """
    #* Arrange
    G = nx.Graph([(0,1), (1,2), (2,3), (0,3), (3,4)])
    s = 1

    expected_node_dep = {3: 1.0, 4: 0.0, 0: 1.0, 2: 1.0, 1: 4.0}

    #* Act
    node_dep = find_node_pair_dependencies(G, s)

    #* Assert
    assert dict(node_dep) == approx(expected_node_dep)

def test_node_pair_dependencies_larger():
    """
    Test node pair dependencies on larger graph
    """
    #* Arrange
    G = nx.Graph([(1,2), (1, 4), (2, 3), (3, 4), (3, 5), (3, 8), (4, 6), (5, 8), (6,7), (7,8)])
    s = 4

    expected_node_dep = {6: 1.0, 7: 0.0, 3: 2.5, 8: 0.0, 5: 0.0, 1: 0.5, 2: 0.0, 4: 7.0}

    #* Act
    node_dep = find_node_pair_dependencies(G, s)

    #* Assert
    assert dict(node_dep) == approx(expected_node_dep)