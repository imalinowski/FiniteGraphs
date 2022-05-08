from collections import deque


def load_graph(path):
    print("Loading...{}".format(path))
    graph = {}  # graph : Dictionary = { node : { node1, node2, node3} }
    f = open(path, "r")
    while True:
        line = f.readline().strip()
        if not line:
            break
        if line.startswith("#"):
            continue
        node_from, node_to = map(int, line.split())

        # since graph is undirected
        if node_from in graph:
            graph[node_from].add(node_to)
        else:
            graph[node_from] = {node_to}

        # since graph is undirected
        if node_to in graph:
            graph[node_to].add(node_from)
        else:
            graph[node_to] = {node_from}

    return graph


def dfs(graph, start, log=False):  # graph : Dictionary = { node : { node1, node2, node3} }
    if log:
        print("dfs from {}".format(start))
    stack, path = deque(), []
    stack.append(start)
    while stack:
        node = stack.pop()
        if node in path:
            continue
        path.append(node)
        for neighbour in graph[node]:
            stack.append(neighbour)
    return path


def find_components(graph):  # graph : Dictionary = { node : { node1, node2, node3} }
    components = []
    used = []
    for node in graph:
        if node not in used:
            path = dfs(graph, node)
            components.append(path)
            used += path
    return components
