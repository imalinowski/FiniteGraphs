from alg_with_files import *
from alg_for_graphs import *
from alg_for_metagraphs import *
import networkx as nx
import matplotlib.pyplot as plt


def test():
    g, gin = load_graph_directed_and_inverse('test_extremal.txt')
    scc_test = find_scc(g, gin, True)

    print(scc_test)


# graph_undirected = load_graph_undirected("web-Google.txt")
# graph_directed, graph_directed_inv = load_graph_directed_and_inverse("web-Google.txt")
# Блок с считыванием графов в память пк
'''
# Блок с считыванием графов в память пк
# Загружаем графы в память компьютера
graph_undirected = load_graph_undirected("web-Google.txt")
graph_directed, graph_directed_inv = load_graph_directed_and_inverse("web-Google.txt")
# Считаем кол-во вершин
# 875713
nodes = len(graph_directed)

# Считаем кол-во ребер
# 5105039
edges = sum(len(i) for i in graph_directed.values())
'''
'''
nodes = 875713
edges = 5105039


# Количество компонент слабой связности
# Занимает где-то 2 минуты
# То, что возвращает find_wcc, находится в файле wcc, загрузили при помощи load_list_to_file
# Для того, чтобы вернуть его в память компьютера, используется load_list_from_file
# count_wcc = 2746
path_wcc = load_list_from_file('wcc.txt')
count_wcc = len(path_wcc)


# Количество компонент сильной связности
# То, что возвращает find_scc, находится в файле scc, загрузили при помощи load_list_to_file
# Для того, чтобы вернуть его в память компьютера, используется load_list_from_file
# count_scc = 176088
# print(len(find_scc(graph_directed, graph_directed_inv, log=True)))
path_scc = load_list_from_file('scc_2.txt')
count_scc = len(path_scc)


# Количество вершин в максимальной компоненте слабой связности
# Посчитать из path_wcc
# count_vertex_wcc = 855802
count_vertex_wcc = -1
for wcc in path_wcc:
    count_vertex_wcc = max(count_vertex_wcc, len(wcc))

# Количество вершин в максимальной компоненте сильной связности
# Посчитать из path_scc
# count_vertex_scc = 371764
count_vertex_scc = 0
for scc in path_scc:
    count_vertex_scc = max(count_vertex_scc, len(scc))

'''

now = time.time()
meta_graph_x = nx.DiGraph()
meta_graph_x.add_edges_from(load_graph_to_list_of_edges('meta_graph_2.txt'))
plt.figure(1, figsize=(65, 65))
pos = nx.spring_layout(meta_graph_x)
nx.draw(meta_graph_x, pos=pos, node_size=2, width=0.2, arrowsize=1)
print('Это заняло ', time.time() - now)
plt.show()

'''

print('Число вершин в графе web-Google: ', nodes)
print('Число ребер в графе web-Google: ', edges)
print('Плотность графа web-Google: ', edges / (nodes * (nodes - 1) / 2))
print('Количество компонент слабой связности: ', count_wcc)
print('Количество компонент сильной связности: ', count_scc)
print('Доля веришин в наибольшей компоненте слабой связности: ', count_vertex_wcc / nodes)
print('Доля веришин в наибольшей компоненте сильной связности: ', count_vertex_scc / nodes)
print()

'''
'''

# А теперь запустим find_scc
now = time.time()
path_scc = find_scc(graph_directed, graph_directed_inv, log=True)
print('О чудо, find_scc закончило свою работу. Это заняло ', time.time() - now)
load_list_to_file(path_scc, 'scc_2.txt')
print('И более того, она загрузила свой список в файл scc_2.txt')
'''
'''

path_scc = load_list_from_file('scc_2.txt')

# Создали граф, где ключ - вершина, значение - номер компоненты
graph_index = create_dict_with_index_scc(path_scc)
print('Создали граф с индексами')
meta_graph = create_metagraph(graph_directed, graph_index)
print('На основе его создали метаграф')
load_list_to_file_for_networks(meta_graph, 'meta_graph_2.txt')
print('И даже загрузили его в файлик')

'''
'''
print('Ответы для А3')

graph_networkx = nx.DiGraph()
graph_networkx.add_edges_from(load_graph_to_list_of_edges('meta_graph.txt', log=True))
nx.draw(graph_networkx)
plt.show()
di_graph = nx.DiGraph()
di_graph.add_edges_from(load_graph_to_list_of_edges('web-Google.txt'))
'''

'''
print("---A.2---")
# На обработку уходит 2 минуты, всегда разные значения
max_component = max(path_wcc, key=len)
print('Шаг один')
max_component = sub_graph(graph_undirected, max_component)
print('Шаг два')
precompute(max_component)
print('Шаг три')
r, d, dist_90 = compute_r_d_90dist(max_component)
print('Шаг четыре')
print('Радиус сети: ', r)
print('Диаметр сети: ', d)
print("90% процентиль: ", dist_90)

print("---A.5---")
# Где-то 48 секунд
min_d, max_d = node_degree(graph_undirected)
print(f"degree : min {min_d} max {max_d}")
print("---------")
'''




