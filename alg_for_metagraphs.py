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

# Возвращает граф в виде списка кортежей, где кортеж - ребро. Считывается из файла списка ребер
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
