# So, тут будет тестовый алгоритм.
import networkx

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

# Вот у нас список, который возвращает find_scc
l = [[1, 5, 7, 8], [2, 3], [4], [6, 9, 10, 12], [11]]
# Название файла
path_to_file = 'scc.txt'

# Это мы его загружаем в файлик
load_list_to_file(l, 'scc.txt', log=True)

# Это мы его выгрузили из файла
new_l = load_list_from_file(path_to_file, log=True)
print(new_l)

# А это мы записали его в словарь
graph_index = create_dict_with_index_scc(new_l, log=True)
print(graph_index)

graph_directed = load_graph_directed('test.txt')
meta_graph = {}
for vertex_1 in graph_directed:
    for vertex_2 in graph_directed[vertex_1]:
        if graph_index[vertex_1] != graph_index[vertex_2]:
            if graph_index[vertex_1] not in meta_graph:
                meta_graph[graph_index[vertex_1]] = set()
            meta_graph[graph_index[vertex_1]].add(graph_index[vertex_2])

print(meta_graph)


# А теперь время его визуализировать


