from algorithms import *
import sys


def test_for_undirected(path):
    print('Загрузка данных\n')
    graph_undirected = load_graph_undirected(path)

    nodes = len(graph_undirected)
    edges = sum(len(i) for i in graph_undirected.values())

    path_wcc = find_wcc(graph_undirected)

    count_wcc = len(path_wcc)

    count_vertex_wcc = -1
    for wcc in path_wcc:
        count_vertex_wcc = max(count_vertex_wcc, len(wcc))

    print('---A.1---')
    print('Число вершин в графе', filename[:-4], ': ', nodes)
    print('Число ребер в графе', filename[:-4], ': ', edges)
    print('Плотность графа', filename[:-4], ': ', edges / (nodes * (nodes - 1) / 2))
    print('Количество компонент слабой связности: ', count_wcc)
    print('Доля веришин в наибольшей компоненте слабой связности: ', count_vertex_wcc / nodes)
    print()

    print("---A.2---")
    # На обработку уходит 2 минуты, всегда разные значения
    max_component = max(path_wcc, key=len)
    max_component = sub_graph(graph_undirected, max_component)
    precompute(max_component)
    r, d, dist_90 = compute_r_d_90dist(max_component)
    print('Радиус сети: ', r)
    print('Диаметр сети: ', d)
    print("90% процентиль: ", dist_90)
    print()

    print('---A.3---')
    print('Граф не является ориентированным, значит метаграф не строим \n')

    print("---A.4---")
    graph_3_cliques = count_k_cliques(graph_undirected, 3)
    local_coeffs = calculate_local_coeffs(graph_3_cliques, graph_undirected)
    average_coeff = calculate_average_coeff(local_coeffs, graph_undirected)
    global_coeff = calculate_global_coeff(local_coeffs, graph_undirected)
    print(f"Количество треугольников: {len(graph_3_cliques)}")
    print(f"Средний кластерный коэффициент сети: {average_coeff}")
    print(f"Глобальный кластерный коэффициент: {global_coeff}\n")

    print("---A.5---")
    min_d, max_d, avg_d = node_degree(graph_undirected)
    print('Минимальная степень вершины: ', min_d)
    print('Максимальная степень вершины: ', max_d)
    print('Средняя степень вершины: ', avg_d)
    print()

    print("---B---")
    calculate_nodes_proportion_random(graph_undirected)
    calculate_nodes_proportion_max_degree(graph_undirected)


def test_for_directed(path):
    print('Загрузка данных')
    graph_undirected = load_graph_undirected(path)
    graph_directed, graph_directed_inv = load_graph_directed_and_inverse(path)

    nodes = len(graph_directed)
    edges = sum(len(i) for i in graph_directed.values())

    path_wcc = find_wcc(graph_undirected)
    path_scc = find_scc(graph_directed, graph_directed_inv)

    count_wcc = len(path_wcc)
    count_scc = len(path_scc)

    count_vertex_wcc = -1
    for wcc in path_wcc:
        count_vertex_wcc = max(count_vertex_wcc, len(wcc))

    count_vertex_scc = 0
    for scc in path_scc:
        count_vertex_scc = max(count_vertex_scc, len(scc))

    print()
    print('---A.1---')
    print('Число вершин в графе', filename[:-4], ': ', nodes)
    print('Число ребер в графе', filename[:-4], ': ', edges)
    print('Плотность графа', filename[:-4], ': ', edges / (nodes * (nodes - 1) / 2))
    print('Количество компонент слабой связности: ', count_wcc)
    print('Количество компонент сильной связности: ', count_scc)
    print('Доля веришин в наибольшей компоненте слабой связности: ', count_vertex_wcc / nodes)
    print('Доля веришин в наибольшей компоненте сильной связности: ', count_vertex_scc / nodes)
    print()

    print("---A.2---")
    # На обработку уходит 2 минуты, всегда разные значения
    max_component = max(path_wcc, key=len)
    max_component = sub_graph(graph_undirected, max_component)
    precompute(max_component)
    r, d, dist_90 = compute_r_d_90dist(max_component)
    print('Радиус сети: ', r)
    print('Диаметр сети: ', d)
    print("90% процентиль: ", dist_90)
    print()

    print('---A.3---')
    # print('Изначальный граф: ', graph_directed)
    # Создали граф, где ключ - вершина, значение - номер компоненты
    graph_index = create_dict_with_index_scc(path_scc)
    print('Создан граф с индексами, где ключ - вершина, значение - номер компоненты')
    # print(graph_index)
    meta_graph = create_metagraph(graph_directed, graph_index)
    print('На основе его создали метаграф')
    # print(meta_graph)
    load_list_to_file_for_networks(meta_graph, 'meta_graph.txt')
    print('В виде списка ребер он находится в файле \'meta_graph.txt\'\n')

    graph_networkx = nx.DiGraph()
    graph_networkx.add_edges_from(load_graph_to_list_of_edges('meta_graph.txt'))
    nx.draw(graph_networkx, node_size=5, node_color='red')
    plt.show()

    print("---A.4---")
    graph_3_cliques = count_k_cliques(graph_undirected, 3)
    local_coeffs = calculate_local_coeffs(graph_3_cliques, graph_undirected)
    average_coeff = calculate_average_coeff(local_coeffs, graph_undirected)
    global_coeff = calculate_global_coeff(local_coeffs, graph_undirected)
    print(f"Количество треугольников: {len(graph_3_cliques)}")
    print(f"Средний кластерный коэффициент сети: {average_coeff}")
    print(f"Глобальный кластерный коэффициент: {global_coeff}\n")

    print("---A.5---")
    min_d, max_d, avg_d = node_degree(graph_undirected)
    print('Минимальная степень вершины: ', min_d)
    print('Максимальная степень вершины: ', max_d)
    print('Средняя степень вершины: ', avg_d)
    print()

    print("---B---")
    calculate_nodes_proportion_random(graph_undirected)
    calculate_nodes_proportion_max_degree(graph_undirected)


filename = sys.argv[1]
if sys.argv[2] == '0':
    test_for_undirected(filename)
elif sys.argv[2] == '1':
    test_for_directed(filename)
