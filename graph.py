f = open("CA-AstroPh.txt", "r")
graph = {}
edges = 0
while True:
    line = f.readline().strip()
    if not line:
        break
    if line.startswith("#"):
        continue
    edges += 1
    nodeFrom, nodeTo = map(int, line.split())
    if nodeFrom in graph:
        graph[nodeFrom].append(nodeTo)
    else:
        graph[nodeFrom] = [nodeTo]
# print("from {} to {}".format(nodeFrom, nodeTo))
# print(graph)
nodes = len(graph)
print("Nodes {}".format(nodes))
print("Edges {}".format(edges))
print("Density {}".format(edges / (nodes * (nodes - 1) / 2)))
