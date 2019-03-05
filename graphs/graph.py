from random import randint


class Graph(object):
    """'
    representation of Graph
    """

    def __init__(self, nodes=None, edges=None):
        self.nodes = nodes or []
        self.edges = edges or []

    def nodes(self):
        """returns the present nodes"""
        return self.nodes

    def edges(self):
        """returns the present edges"""
        return self.edges

    def add_node(self, node):
        """Add node to the graph if node is not present.
        :param node: {Node}
        """
        if node not in self.nodes:
            self.nodes.append(node)

    def add_edge(self, edge):
        if edge.node1 in self.nodes and edge.node2 in self.nodes:
            if edge not in self.edges:
                self.edges.append(edge)


class Node(object):
    def __init__(self, id=None):
        self.id = id or randint(0, 100)

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return self.id.__str__()

    def __repr__(self):
        return self.id.__str__()


class Edge(object):
    def __init__(self, node1=None, node2=None):
        self.node1 = node1 or Node(randint(0, 100))
        self.node2 = node2 or Node(randint(0, 100))

    def __eq__(self, other):
        return (
                       self.node1 == other.node1 and self.node2 == other.node2) or (
                       self.node1 == other.node2 and self.node2 == other.node1)

    def __repr__(self):
        return "[" + (self.node1.__str__()) + "," + (
            self.node2.__str__()) + "]"

    def __str__(self):
        return "[" + (self.node1.__str__()) + "," + (
            self.node2.__str__()) + "]"


# example
g = Graph()
g.add_edge(Edge(Node(2), Node(2)))
g.add_edge(Edge(Node(2), Node(2)))
g.add_node(Node(3))
g.add_edge(Edge(Node(2), Node(3)))
g.add_edge(Edge(Node(2), Node(5)))

print(f'nodes {g.nodes}')
print(f'edges {g.edges}')
