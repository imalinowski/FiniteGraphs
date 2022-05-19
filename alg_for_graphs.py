from collections import deque
import heapq
import time
from typing import Dict
import random
import matplotlib.pyplot as plt


# dfs, который возвращает вершины, которые смог посетить
def dfs(graph, start, log=False):
    now = time.time()
    if log:
        print("dfs from {}".format(start))
    stack, path = deque(), set()
    stack.append(start)
    while stack:
        node = stack.pop()
        if node in path:
            continue
        path.add(node)
        for neighbour in graph[node]:
            stack.append(neighbour)
    if log:
        print('Done dfs')
        print("# finding components took {} sec #".format(time.time() - now))
    return path


# dfs, который считает время выхода для каждой вершины
# Разобрать обязательно
graph_time = 0
def dfs_with_time(graph, start, used, time_in, time_out, log=False):
    global graph_time
    now = time.time()
    counter = 0
    if log:
        print("dfs from {}".format(start))

    stack = deque()
    stack.append((0, start))
    while stack:
        task = stack.pop()
        graph_time += 1

        node = 0
        if task[0] == 0:
            node = task[1]
            counter += 1
        elif task[0] == 1:
            time_out[task[1]] = graph_time
            continue

        if node in used:
            continue

        used.add(node)

        stack.append((1, node))
        time_in[node] = graph_time

        for neighbour in graph[node]:
            stack.append((0, neighbour))

    if log:
        print('Done dfs')
        print('Visited: ', counter)
        print("# finding components took {} sec #".format(time.time() - now))


# dfs, в котором мы передаем уже поситившиеся вершины
def dfs_inverse(graph, start, used, log=False):
    now = time.time()

    counter = 0
    if log:
        print("dfs from {}".format(start))
    stack, path = deque(), set()
    stack.append(start)
    while stack:
        node = stack.pop()

        if node in used:
            continue

        used.add(node)
        path.add(node)
        stack.append(node)

        for neighbour in graph[node]:
            if neighbour not in used:
                stack.append(neighbour)

    if log:
        print('Done dfs')
        print('Visited: ', counter)
        print("# finding components took {} sec #".format(time.time() - now))

    return path


# Находим все компоненты слабой связности в виде списка списков
def find_wcc(graph, log=False):
    now = time.time()
    components = []
    used = set()
    for node in graph:
        if node not in used:
            path = dfs(graph, node, log=False)
            used = used | path
            components.append(path)
    if log:
        print("# finding components took {} sec #".format(time.time() - now))
    return components  # return sub graphs witch belongs to single component


# Находим все компоненты сильной связности в виде списка списков
def find_scc(graph, graph_inverse, log=False):
    now = time.time()

    time_in = {x: 0 for x in graph}
    time_out = {x: 0 for x in graph}

    used = set()
    for node in graph:
        if node not in used:
            dfs_with_time(graph, node, used, time_in, time_out, log=False)

    if log:
        print("30% done")

    priority = []
    for vertex in time_out:
        heapq.heappush(priority, (-time_out[vertex], vertex))

    components = []
    used.clear()

    if log:
        print("50% done")

    while priority:
        t, v = heapq.heappop(priority)
        if v not in used:
            path = dfs_inverse(graph_inverse, v, used, log=False)
            used = used | path
            components.append(path)

    if log:
        print("# finding components took {} sec #".format(time.time() - now))
    return components


# -------------------------------------------- #
#     Не мои алгоритмы для заданий 2 и 5       #
# -------------------------------------------- #

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


def node_degree(graph: dict):
    min_d = len(min(graph.values(), key=len))
    max_d = len(max(graph.values(), key=len))
    distribution = dict()
    for i in graph.values():
        degree = len(i)
        if degree in distribution:
            distribution[degree] += 1
        else:
            distribution[degree] = 1
    degree = list(distribution.keys())
    nums = list(distribution.values())
    plt.ylabel('degree of a node')
    plt.xlabel('number of nodes')
    plt.plot(degree, nums, 'ro')
    plt.show()
    plt.loglog(degree, nums, 'ro')
    plt.ylabel('degree of a node')
    plt.xlabel('number of nodes')
    plt.show()
    return min_d, max_d


def sub_graph(graph: dict, nodes):
    subgraph = {}
    for v in nodes:
        subgraph[v] = graph[v]
    return subgraph


class Node:

    def __init__(self, key):
        self.key = key
        self.parents: Dict[int, int] = {}  # dictionary of parents to landmarks

    def parent_to(self, u, v):  # parent v to landmark u
        self.parents[u] = v


NODES: Dict[int, Node] = {}  # dic of pairs key:Node
landmarks = set()


def precompute(graph, log=False):
    for _ in range(3):  # more landmarks - less error, but more time
        landmarks.add(random.choice(list(graph.keys())))
    for u in landmarks:
        parent_to_u = bfs(graph, u)
        if log:
            print("path to {} is {}".format(u, parent_to_u))
        for node in parent_to_u.keys():
            if node not in NODES.keys():
                NODES[node] = Node(node)
            NODES[node].parent_to(u, parent_to_u[node])


def path_to(u: int, s: int, log=False):
    path = [s]
    if log:
        print("path {} to {}".format(u, str(s)))
        print("NODES[s]{}".format(NODES[s].parents.keys()))
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
    subgraph = {}
    for u in landmarks:
        add_path_to_graph(subgraph, path_to(u, s, log), log)
        add_path_to_graph(subgraph, path_to(u, t, log), log)

    if log:
        print("sub graph {}".format(subgraph))

    # using bfs compute path in subgraph
    parent_to_t = bfs(subgraph, t)
    path = [s]
    node = s
    while node != t:
        node = parent_to_t[node]
        path.append(node)

    return path


def compute_r_d_90dist(graph, log=False):
    if log:
        print("compute_r_d_90dist graph {}".format(graph))
    nodes = set()
    for _ in range(500):
        nodes.add(random.choice(list(graph.keys())))
    distances = []
    if log:
        print("compute_r_d_90dist nodes {}".format(nodes))
    nodes = list(nodes)
    for u in range(len(nodes) - 1):
        dist = 0
        for v in range(u + 1, len(nodes)):
            dist = max(dist, len(landmarks_bfs(nodes[u], nodes[v])))
        distances.append(dist)
    distances.sort()
    dist90 = distances[round(0.9 * len(distances))]
    return distances[0], distances[len(distances) - 1], dist90
