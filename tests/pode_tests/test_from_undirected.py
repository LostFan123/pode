import networkx as nx
from hypothesis import (assume,
                        given,
                        note)

from pode.pode import Graph
from tests.strategies.graphs import unordered_graphs


@given(unordered_graphs)
def test_data_preservation(graph: nx.Graph) -> None:
    ordered_graph = Graph.from_undirected(graph)
    assert set(graph) == set(ordered_graph)
    assert all(edge in graph.edges for edge in ordered_graph.edges)
    assert all(ordered_graph.edges[edge]['side'] == graph.edges[edge]['side']
               for edge in ordered_graph.edges)


@given(unordered_graphs)
def test_bidirected_edges(graph: nx.Graph) -> None:
    ordered_graph = Graph.from_undirected(graph)
    ordered_edges = map(tuple, map(sorted, ordered_graph.edges))
    assert len(ordered_graph.edges) == len(set(ordered_edges))


@given(unordered_graphs)
def test_outcoming_edges(graph: nx.Graph) -> None:
    note(f"Nodes: {list(graph)}")
    note(f"Edges: {list(graph.edges)}")
    assume(len(graph) > 1)
    ordered_graph = Graph.from_undirected(graph)
    *nodes, last_node = list(ordered_graph)
    assert all(len(ordered_graph[node]) == 1 for node in nodes[:-1])
    assert not ordered_graph[last_node]
