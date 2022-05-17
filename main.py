import alg

# graph_undirected = alg.load_graph_undirected("web-Google.txt")
# graph_directed, graph_directed_inv = alg.load_graph_directed_and_inverse("web-Google.txt")

# nodes = len(graph_directed)
nodes = 875713

# edges = sum(len(i) for i in graph_directed.values())
edges = 5105039

# Количество компонент слабой связности
# print(len(alg.find_wcc(graph_undirected, log=True)))
count_wcc = 2746

# Количество компонент сильной связности
# print(len(find_scc(graph_directed, graph_directed_inv, log=True)))
count_scc = 176088

# Количество вершин в компоненте слабой связности
count_vertex_wcc = 855802

# Количество вершин в компоненте сильной связности
# Посчитать!!!
count_vertex_scc = 434818


print('Число вершин в графе web-Google: ', nodes)
print('Число ребер в графе web-Google: : ', edges)
print('Плотность графа web-Google: ', edges / (nodes * (nodes - 1) / 2))
print('Количество компонент слабой связности: ', count_wcc)
print('Количество компонент сильной связности: ', count_scc)
print('Доля веришин в наибольшей компоненте слабой связности: ', count_vertex_wcc / nodes)
print('Доля веришин в наибольшей компоненте сильной связности: ', count_vertex_scc / nodes)
