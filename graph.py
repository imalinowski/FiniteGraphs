import algorithms
import time
import sys

filename = sys.argv[1] if(len(sys.argv) >= 2) else "test_graph_1.txt"
graph = algorithms.load_graph(filename)
# graph = algorithms.load_graph("CA-AstroPh.txt")

nodes = len(graph)
edges = sum(len(i) for i in graph.values())

print("---A.1---")
print("Nodes {}".format(nodes))
print("Edges {}".format(edges))
print("Density {}".format(edges / (nodes * (nodes - 1) / 2)))
components = algorithms.find_components(graph)
print("Components {}".format(len(components)))
max_component = max(components, key=len)
print("Max component {}% of all nodes".format(
    len(max_component) / nodes * 100
))
print("---A.2---")
max_component = algorithms.sub_graph(graph, max_component)
algorithms.precompute(max_component)
r, d, dist_90 = algorithms.compute_r_d_90dist(max_component)
print("r {}".format(r))
print("d {}".format(d))
print("90 % distance {}".format(dist_90))
print("---A.5---")
min_d, max_d, average = algorithms.node_degree(graph)
print(f"degree : min {min_d} max {max_d} average {average}")
print("---------")