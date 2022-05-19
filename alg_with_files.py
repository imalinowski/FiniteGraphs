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


# Загружаем граф как инвертированный
# Уже не используется
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


# Загружает список списков в файл для последующей работы с ним
# Нужно для записи графа в файл после find_scc и find_wcc
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


# Считываем из файла в список списков, где элемент списка - все вершины сильной связности
# Нужно для выгрузки find_scc из scc.txt
def load_list_from_file(path_to_file, log=False):
    if log:
        print('Считываю из файла в список')
    file = open(path_to_file, "r")
    l_new = [list(map(int, line.split())) for line in file]
    if log:
        print('Процесс списывания успешно завершен')
    return l_new


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
