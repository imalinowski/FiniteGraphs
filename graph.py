import algorithms
import time

# graph = algorithms.load_graph("CA-AstroPh.txt")
graph = algorithms.load_graph("test_graph_1.txt")

nodes = len(graph)
edges = sum(len(i) for i in graph.values())

print("---A.1---")
print("Nodes {}".format(nodes))
print("Edges {}".format(edges))
print("Density {}".format(edges / (nodes * (nodes - 1) / 2)))
components = algorithms.find_components(graph)
print("Components {}".format(len(components)))
print("Max component {}% of all nodes".format(
    len(max(components, key=len))/nodes * 100
))
print("---------")

# print(graph)
# path = algorithms.dfs(graph, min(graph.keys()))
# cur = time.time() * 1000
# path = algorithms.dfs(graph, 3)
# print("time {}".format((time.time() * 1000 - cur)))
# print(path)
