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


def precompute(graph: dict, log=False):
    landmarks = [random.choice(list(graph.keys())) for _ in range(3)]
    for u in landmarks:
        parent_to_u = bfs(graph, u)
        if log:
            print("path to {} is {}".format(u, parent_to_u))
        for node in parent_to_u.keys():
            if node not in NODES.keys():
                NODES[node] = Node(node)
            NODES[node].parent_to(u, parent_to_u[node])


def path_to_u(u: int, s: int):
    path = [s]
    if u not in NODES[s].parents:
        raise ValueError('{} is not in U nodes'.format(u))
    while s != u:
        s = NODES[s].parents[u]
        path.append(s)
    return path
