import random


class Graph:
    """
    Class to hold graph

    On instantiation the vertices get extracted and the degrees are calculated and stored for each vertex
    """

    def __init__(self, edges, vs=None):
        self.edges = edges

        # calculate vertices from given edges
        self.vertices = vs if vs is not None else {[e[0] for e in self.edges] + [e[1] for e in self.edges]}

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

    # used vertices
    clique = [vertex for vertex in graph.vertices]

    c_edges = {edge for edge in graph.edges}

    # sort by degrees and only keep vertex names
    sorted_degrees = [x[0] for x in sorted(graph.degrees.items(), key=lambda el: el[1], reverse=True)]

    last_size = len(c_edges)
    for v in sorted_degrees:
        if v not in clique:
            continue

        # could be optimized...
        inner_edges = [edge for edge in c_edges if edge[0] == v or edge[1] == v]

        # make sure that no unwanted vertices are accidentally added
        # and v has to be included even when there were no edges
        clique = set([x[0] for x in inner_edges] + [x[1] for x in inner_edges]).intersection(clique).union({v})
        c_edges = [edge for edge in graph.edges if edge[0] in clique or edge[1] in clique]

        # corrections due to apparently wrong algorithm in slides
        # only terminate when "clique" is actually a clique
        if len(c_edges) == last_size and is_clique(clique, graph):
            break

        last_size = len(c_edges)

    return clique


def is_clique(clique, graph):
    """
    Check if given vertices are part of a clique in given graph "graph"
    :param clique:
    :param graph:
    :return: True if vertices "clique" form a clique
            False otherwise
    """
    for v1 in clique:
        for v2 in clique:
            if v1 != v2 and (v1, v2) not in graph.edges and (v2, v1) not in graph.edges:
                return False

    return True


def gen_random_graph_with_clique(size, clique_size, r):
    """
    Generates graph with a clique of size clique_size containing randomly selected vertices.

    :param size: size of the returned graph
    :param clique_size: size of the clique contained in the graph. Must not be greater than the size parameter
    :param r: Each vertex (considering a complete graph) is added with a probability of r or when part of the predefined
     clique
    :return: Graph object containing a graph with a cliques_size clique
    """
    vertices = [v for v in range(1, size + 1)]
    g_edges = []

    clique = random.sample(vertices, clique_size)

    degrees = {vn: (clique_size if vn in clique else 0) for vn in vertices}

    # create clique
    for i in range(0, len(vertices) - 1):
        vi = vertices[i]
        for j in range(i + 1, len(vertices)):
            vj: int = vertices[j]
            if vi in clique and vj in clique:
                g_edges.append((vi, vj))

    # add other edges
    for i in range(0, len(vertices)-1):
        vi = vertices[i]
        for j in range(i+1, len(vertices)):
            vj: int = vertices[j]

            if r >= random.random() \
                    and (degrees[vi] < clique_size - 1 or degrees[vj] < clique_size - 1) \
                    and not (vi in clique and vj in clique):
                g_edges.append((vi, vj))
                degrees[vi] += 1
                degrees[vj] += 1

    return Graph(g_edges, set(vertices))
