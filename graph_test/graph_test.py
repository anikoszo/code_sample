from graphs.graph import Node, Edge, Graph


def test_add_node():
    graph = Graph()
    graph.add_node(Node(1))
    assert len(graph.nodes) == 1
    graph.add_node(Node(2))
    assert len(graph.nodes) == 2
    graph.add_node(Node(2))
    assert len(graph.nodes) == 2


def test_add_edge():
    graph = Graph()
    graph.add_edge(Edge(Node(2), Node(2)))
    assert len(graph.edges) == 0
    graph.add_edge(Edge(Node(5), Node(2)))
    assert len(graph.edges) == 0
    graph.add_node(Node(2))
    graph.add_edge(Edge(Node(2), Node(2)))
    assert len(graph.edges) == 1
    graph.add_node(Node(5))
    graph.add_edge(Edge(Node(2), Node(5)))
    assert len(graph.edges) == 2
    graph.add_edge(Edge(Node(5), Node(2)))
    assert len(graph.edges) == 2
