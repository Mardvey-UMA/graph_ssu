from Graph_cotainer import Graph, graph_path
import os
os.chdir(graph_path)
graph = Graph.console_input()
print(graph)
n1, n2 = input("Введите два узла").split()
paths, shortest_length = graph.task21(n1, n2)