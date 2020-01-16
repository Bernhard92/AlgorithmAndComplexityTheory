import random


class Graph:
    """
    Class to hold graph

    On instantiation the vertices get extracted and the degrees are calculated and stored for each vertex
    """

    def __init__(self, edges):
        self.edges = edges

        # calculate vertices from given edges
        self.vertices = set([e[0] for e in self.edges] + [e[1] for e in self.edges])

        self.degrees = {vn: 0 for vn in self.vertices}

        for e in self.edges:
            self.degrees[e[0]] += 1
            self.degrees[e[1]] += 1


def get_clique(graph):
    """
    Tries to find largest clique using the greedy algorithm described on slide 4-25.

    :param graph:
    :return:
    """

    clique = [vertex for vertex in graph.vertices]

    c_edges = set(edge for edge in graph.edges)

    # sort by degrees and only keep vertex names
    sorted_degrees = [x[0] for x in sorted(graph.degrees.items(), key=lambda el: el[1], reverse=True)]

    last_size = len(c_edges)
    for v in sorted_degrees:
        if v not in clique:
            continue

        # could be optimized...
        inner_edges = [edge for edge in c_edges if edge[0] == v or edge[1] == v]
        clique = set([x[0] for x in inner_edges] + [x[1] for x in inner_edges])
        c_edges = [edge for edge in graph.edges if edge[0] in clique or edge[1] in clique]

        if c_edges == last_size:
            break

        last_size = len(c_edges)

    return clique


def gen_random_graph_with_clique(size, clique_size, r):
    """
    Generates graph with a clique of size clique_size containing randomly selected vertices.

    :param size: size of the returned graph
    :param clique_size: size of the clique contained in the graph. Must not be greater than the size parameter
    :param r: Each vertex (considering a complete graph) is added with a probability of r or when part of the predefined
     clique
    :return: Graph object containing a graph with a cliques_size clique
    """
    v = [v for v in range(1, size + 1)]
    g_edges = []

    clique = random.sample(v, clique_size)

    for i in range(0, len(v)-1):
        vi = v[i]
        for j in range(i+1, len(v)):
            vj: int = v[j]

            if r >= random.random() or vi in clique and vj in clique:
                g_edges.append((vi, vj))

    return Graph(g_edges)
