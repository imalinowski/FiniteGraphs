from collections import deque
import heapq
import time
import networkx as nx
from matplotlib import pyplot as plt


# Загружаем граф как неориентированный
def load_graph_undirected(path):
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


# Загружаем граф как ориентированный
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


# Загружаем граф как ориентированный и инвертированный
def load_graph_directed_invers(path):
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

        if node_to not in graph:
            graph[node_to] = set()

        graph[node_to].add(node_from)

    return graph


# Загружаем граф прямым и инвертированным
def load_graph_directed_and_inverse(path):
    print("Loading...{}".format(path))
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
def dfs_with_time(graph, start, used, time_in, time_out, graph_time, log=False):
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


max_len_wss = -1
# Находим все компоненты слабой связности в виде списка списков
def find_wcc(graph, log=False):
    now = time.time()
    components = []
    used = set()
    global max_len_wss
    for node in graph:
        if node not in used:
            path = dfs(graph, node, log=True)
            max_len_wss = max(max_len_wss, len(path))
            used = used | path
            components.append(path)
    if log:
        print("# finding components took {} sec #".format(time.time() - now))
    return components  # return sub graphs witch belongs to single component


# Находим все компоненты сильной связности в виде списка списков
def find_scc(graph, graph_inverse, log=False):
    now = time.time()
    components = []

    graph_time = 0

    time_in = {x: 0 for x in graph}
    time_out = {x: 0 for x in graph}

    used = set()
    trees = []
    for node in graph:
        if node not in used:
            dfs_with_time(graph, node, used, time_in, time_out, graph_time, log=True)

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


# Загружает список списков в файл для последующей работы с ним
def load_list_to_file(l, path_to_file, log=False):
    if log:
        print('Запись начата успешно')

    f = open(path_to_file, 'w')

    for path in l:
        for elem in path:
            f.write(str(elem) + ' ')
        f.write('\n')

    f.close()

    if log:
        print('Запись прошла успешно')


# Загружает в файл граф как список ребер из словаря вида {node: {node, node, node}}
def load_list_to_file_for_networks(graph_dict, path_to_file, log=False):
    if log:
        print('Запись графа для networks начата успешно')

    f = open(path_to_file, 'w')

    for vertex in graph_dict:
        for elem in graph_dict[vertex]:
            f.write(str(vertex) + ' ' + str(elem) + '\n')

    f.close()

    if log:
        print('Запись прошла успешно')


# Считываем из файла в словарь, где ключ - вершина, значение - номер компоненты
def load_list_from_file(path_to_file, log=False):
    if log:
        print('Считываю из файла в список')
    file = open(path_to_file, "r")
    l_new = [list(map(int, line.split())) for line in file]
    if log:
        print('Процесс списывания успешно завершен')
    return l_new


# А это у нас функция для создания словаря, где вершина - ключ, значение - номер компоненты
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


# Создадим загрузку, которая делает список ребер
def load_graph_to_list_of_edges(path, log=False):
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


# Скачали оригинальные файлы
graph_directed, graph_directed_inv = load_graph_directed_and_inverse("web-Google.txt")
'''
# scc_path - список списков компонент сильной связности
scc_path = find_scc(graph_directed, graph_directed_inv, log=True)
print(len(scc_path))
print('Должен быть одинаковым со следующей строкой, либо 176088, либо 255136')
# Загружаем его в файлик
load_list_to_file(scc_path, 'scc.txt', log=True)
'''

# На всякий случай из файлика тоже загружаем
scc_path = load_list_from_file('scc.txt')
print(len(scc_path))
# Создаем словарь с индексами вершин по scc
graph_index = create_dict_with_index_scc(scc_path, log=True)
# В meta_graph записываем наш новый мета-граф
meta_graph = {}

for vertex_1 in graph_directed:
    for vertex_2 in graph_directed[vertex_1]:
        if graph_index[vertex_1] != graph_index[vertex_2]:
            if graph_index[vertex_1] not in meta_graph:
                meta_graph[graph_index[vertex_1]] = set()
            meta_graph[graph_index[vertex_1]].add(graph_index[vertex_2])

print(len(meta_graph))

# Не ту функцию на считывание запустил, как приду, запустить правильную функцию.
# Надо ли с коллабом что-то делать? Крайне не уверен, уверен в обратном


# А теперь попробуем поработать с networks
graph_networkx = nx.DiGraph()
graph_networkx.add_edges_from(load_graph_to_list_of_edges('meta_graph.txt', log=True))
nx.draw(graph_networkx)
plt.show()
