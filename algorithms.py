from collections import deque
from typing import List, Dict
import random


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
        if node_from not in graph:
            graph[node_from] = set()
        if node_to not in graph:
            graph[node_to] = set()

        graph[node_from].add(node_to)
        graph[node_to].add(node_from)

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
            used += path

            sub_graph = {}
            for v in path:
                sub_graph[v] = graph[v]
            components.append(sub_graph)

    return components  # return sub graphs witch belongs to single component


# to do nice to make command to illustrate work
# bfs witch stores the parent in bfs tree
def bfs(graph, start: int, log=False):  # graph : Dictionary = { node : { node1, node2, node3} }
    if log:
        print("bfs from {}".format(start))
    queue, path = [], {}  # path : a pair of node : parent to start in tree
    queue.append(start)
    path[start] = start
    while queue:
        node = queue.pop(0)
        for neighbour in graph[node]:
            if neighbour not in path.keys():
                queue.append(neighbour)
                path[neighbour] = node
    return path


# ----------------------------------------LANDMARK-BFS----------------------------------------

class Node:

    def __init__(self, key):
        self.key = key
        self.parents: Dict[int, int] = {}  # dictionary of parents to landmarks

    def parent_to(self, u, v):  # parent v to landmark u
        self.parents[u] = v


NODES: Dict[int, Node] = {}  # dic of pairs key:Node
landmarks = set()


def precompute(graph, log=False):
    # for _ in range(500):
    #    landmarks.add(random.choice(list(graph.keys())))
    landmarks.add(6)
    for u in landmarks:
        parent_to_u = bfs(graph, u)
        if log:
            print("path to {} is {}".format(u, parent_to_u))
        for node in parent_to_u.keys():
            if node not in NODES.keys():
                NODES[node] = Node(node)
            NODES[node].parent_to(u, parent_to_u[node])


def path_to(u: int, s: int):
    path = [s]
    if u not in NODES[s].parents.keys():
        raise ValueError('{} is not in landmarks nodes {}'.format(u, list(NODES[s].parents.keys())))
    while s != u:
        s = NODES[s].parents[u]
        path.append(s)
    return path


def add_path_to_graph(graph: Dict[int, set], path: list, log=False):
    last = None
    if log:
        print("add path to sub graph {}".format(path))
    for node in path:
        if node not in graph.keys():
            graph[node] = set()
        if last is not None:
            graph[last].add(node)
            graph[node].add(last)
        last = node


def landmarks_bfs(s, t, log=False):
    sub_graph = {}
    for u in landmarks:
        add_path_to_graph(sub_graph, path_to(u, s), log)
        add_path_to_graph(sub_graph, path_to(u, t), log)

    if log:
        print("sub graph {}".format(sub_graph))

    # using bfs compute path in subgraph
    parent_to_t = bfs(sub_graph, t)
    path = [s]
    node = s
    while node != t:
        node = parent_to_t[node]
        path.append(node)

    return path
