from collections import deque
import time
from typing import Dict
import random
import matplotlib.pyplot as plt
import networkx as nx
import heapq


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


# bfs witch stores the parent in bfs tree save_dist - flag to save distances to start
def bfs(graph, start: int, save_dist=False, log=False):  # graph : Dictionary = { node : { node1, node2, node3} }
    if log:
        print("bfs from {}".format(start))
    queue, path = [], {}  # path : a pair of node : parent to start in tree
    queue.append(start)
    path[start] = start

    dist = {}
    if save_dist:
        dist[start] = 0  # path : a pair of node : distance to start in tree

    while queue:
        node = queue.pop(0)
        for neighbour in graph[node]:
            if neighbour in path.keys():
                continue
            queue.append(neighbour)
            path[neighbour] = node

            if save_dist:
                dist[neighbour] = dist[node] + 1

    return path, dist if save_dist else path


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
    # print("PLEASE! IN CASE YOU ARE RUNNING FROM TERMINAL > SAVE AND CLOSE CURRENT SHOWING PICTURE!")
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
        self.dist: Dict[int, int] = {}  # dictionary of distances to landmarks

    def parent_to(self, u, v):  # parent v to landmark u
        self.parents[u] = v

    def dist_to(self, u, d):  # distance d to landmark u
        self.dist[u] = d


NODES: Dict[int, Node] = {}  # dic of pairs key:Node
landmarks = set()


def precompute(graph, log=False):
    for _ in range(3):  # more landmarks - less error, but more time
        landmarks.add(random.choice(list(graph.keys())))
    for u in landmarks:
        parent_to_u, dist_to_u = bfs(graph, u, save_dist=True, log=log)
        if log:
            print("path to {} is {}".format(u, parent_to_u))
        for node in parent_to_u.keys():
            if node not in NODES.keys():
                NODES[node] = Node(node)
            NODES[node].parent_to(u, parent_to_u[node])
            NODES[node].dist_to(u, dist_to_u[node])


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


def landmarks_basic(s: int, t: int):
    dist = len(NODES)
    for u in landmarks:
        d = NODES[s].dist[u] + NODES[t].dist[u]
        if d < dist:
            dist = d
    return dist


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
        print("compute_r_d_90dist landmarks {}".format(landmarks))

    nodes = list(nodes)
    for u in range(len(nodes) - 1):
        dist = 0
        for v in range(u + 1, len(nodes)):
            # dist = max(dist, len(landmarks_bfs(nodes[u], nodes[v])))
            dist = max(dist, landmarks_basic(nodes[u], nodes[v]))
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
# Алгоримы Величко Кирилла

# Загружаем граф как неориентированный
def load_graph_undirected(path):
    print('Загружаем граф как неориентированный')
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


# Загружаем граф как ориентированный
# Уже не используется
def load_graph_directed(path):
    print("Loading...{}".format(path))
    graph = {}  # graph : Dictionary = {node : {node1, node2, node3}}

    f = open(path, "r")
    while True:
        # Прочитали очередную строчку,
        line = f.readline().strip()
        if not line:
            break
        if line.startswith("#"):
            continue
        # Ну а это соответственно откуда и куда
        node_from, node_to = map(int, line.split())


        if node_from not in graph:
            graph[node_from] = set()

        graph[node_from].add(node_to)

    return graph


# Загружаем граф прямым и инвертированным
def load_graph_directed_and_inverse(path):
    print('Загружаем граф как ориентированный прямой и обратный')
    graph, graph_inverse = {}, {}

    f = open(path, "r")
    while True:
        # Прочитали очередную строчку,
        line = f.readline().strip()
        if not line:
            break
        if line.startswith("#"):
            continue
        # Ну а это соответственно откуда и куда
        node_from, node_to = map(int, line.split())

        if node_from not in graph:
            graph[node_from] = set()
        if node_to not in graph:
            graph[node_to] = set()

        if node_from not in graph_inverse:
            graph_inverse[node_from] = set()
        if node_to not in graph_inverse:
            graph_inverse[node_to] = set()


        graph[node_from].add(node_to)
        graph_inverse[node_to].add(node_from)

    return graph, graph_inverse


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


# Функция для создания словаря, где вершина - ключ, значение - номер компоненты
def create_dict_with_index_scc(l, log=False):
    if log:
        print('Создаем необходимый словарь для мета-графа')
    graph_index = {}
    number_of_component = 0
    for path in l:
        number_of_component += 1
        for elem in path:
            graph_index[elem] = number_of_component
    return graph_index


# На вход подается изначальный граф, на выходе получаем метаграф в виде {node: {node, node, node}}
# Возвращает метаграф вида {node : {node, node, node}}, на вход - изначальный граф и граф с индексами компонент
def create_metagraph(graph_directed, graph_index, log=False):
    meta_graph = {}
    for vertex_1 in graph_directed:
        for vertex_2 in graph_directed[vertex_1]:
            if graph_index[vertex_1] != graph_index[vertex_2]:
                if graph_index[vertex_1] not in meta_graph:
                    meta_graph[graph_index[vertex_1]] = set()
                meta_graph[graph_index[vertex_1]].add(graph_index[vertex_2])

    return meta_graph


# Загружает в файл граф как список ребер из словаря вида {node: {node, node, node}}
# Нужно для выгрузки в файл метаграфа для последующей работы с ним
def load_list_to_file_for_networks(meta_graph, path_to_file, log=False):
    if log:
        print('Запись графа для networks начата успешно')

    f = open(path_to_file, 'w')

    for vertex in meta_graph:
        for elem in meta_graph[vertex]:
            f.write(str(vertex) + ' ' + str(elem) + '\n')

    f.close()

    if log:
        print('Запись прошла успешно')


# Возвращает граф в виде списка кортежей, где кортеж - ребро. Считывается из файла списка ребер
def load_graph_to_list_of_edges(path, log=False):
    if log:
        print("Loading...{}".format(path))
    graph = []  # graph : Dictionary = {node : {node1, node2, node3}}

    f = open(path, "r")
    while True:
        # Прочитали очередную строчку,
        line = f.readline().strip()
        if not line:
            break
        if line.startswith("#"):
            continue
        # Ну а это соответственно откуда и куда
        node_from, node_to = map(int, line.split())

        graph.append((node_from, node_to))

    if log:
        print('В памяти компьютера метаграф в виде списка кортежей')

    return graph