from collections import defaultdict


class Graph:
    def __init__(self):
        self.number_of_nodes = 0  # No. of vertices
        self.number_of_edges = 0
        self.graph = defaultdict(list)  # default dictionary to store graph

    def get_number_of_nodes(self):
        return self.number_of_nodes

    def get_number_of_edges(self):
        return self.number_of_edges

    def add_edge(self, node_from, node_to):
        self.graph[node_from].append(node_to)

    def get_neighbors(self, v):
        return self.graph.get(v)

    # Function that returns reverse (or transpose) of this graph
    def get_transpose(self):
        g = Graph()
        # Recur for all the vertices adjacent to this vertex
        for i in self.graph:
            for j in self.graph[i]:
                g.add_edge(j, i)
        g.set_number_of_nodes(self.number_of_nodes)
        g.set_number_of_edges(self.number_of_edges)
        return g

    def set_number_of_nodes(self, total_node_number):
        self.number_of_nodes = total_node_number

    def set_number_of_edges(self, total_edge_number):
        self.number_of_edges = total_edge_number
