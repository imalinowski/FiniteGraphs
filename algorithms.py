from collections import deque
import time
from typing import Dict
import random
import matplotlib.pyplot as plt


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
    stack, path = deque(), set()
    stack.append(start)
    while stack:
        node = stack.pop()
        if node in path:
            continue
        path.add(node)
        for neighbour in graph[node]:
            stack.append(neighbour)
    return path


def find_components(graph, log=False):  # graph : Dictionary = { node : { node1, node2, node3} }
    now = time.time()
    components = []
    used = []
    for node in graph:
        if node not in used:
            path = dfs(graph, node)
            used += path
            components.append(path)
    if log:
        print("# finding components took {} sec #".format(time.time() - now))
    return components  # return sub graphs witch belongs to single component


def sub_graph(graph: dict, nodes):
    subgraph = {}
    for v in nodes:
        subgraph[v] = graph[v]
    return subgraph


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


def node_degree(graph: dict, log=False):
    if log:
        print(f"graph >{graph}")
    min_d = len(min(graph.values(), key=len))
    average = round(sum([len(i) for i in graph.values()]) / len(graph.values()))
    max_d = len(max(graph.values(), key=len))
    if log:
        print(f"min {min_d}  max {max_d} average {average}")
    distribution = dict()
    for i in graph.values():
        degree = len(i)
        if degree in distribution:
            distribution[degree] += 1
        else:
            distribution[degree] = 1
    degree = list(distribution.keys())

    nums = []
    for n in list(distribution.values()):
        nums.append(n / len(graph.keys()))
    plt.xlabel('degree of a node')
    plt.ylabel('number of nodes')
    plt.plot(degree, nums, 'ro')
    print("PLEASE! SAVE AND CLOSE CURRENT SHOWING PICTURE!")
    plt.show()
    plt.loglog(degree, nums, 'ro')
    plt.xlabel('degree of a node')
    plt.ylabel('number of nodes')
    plt.show()
    return min_d, max_d, average


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


# ----------------------------------------------------------------------------------------

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

# r 6 d 14 90d 12
# r 7 d 14 90d 12
# r 7 d 13 90d 11
# r 7 d 15 90d 12

# r 6 d 14 90d 12
# r 7 d 17 90d 13
# r 5 d 14 90d 12
# r 6 d 16 90d 15

# --------------------------------------------------------------------------------------------
