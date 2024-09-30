# 3. Для каждой вершины графа вывести её степень.
from Graph_cotainer import Graph, graph_path
import os
os.chdir(graph_path)
graph = Graph.console_input()
for node in graph.adjacency_list.keys():
    if graph.directed:
        outcoming = len(graph.adjacency_list[node])
        incoming = len([n for n, neighbors in graph.adjacency_list.items() if node in neighbors])
        print(f"-deg({node}) = {outcoming}")
        print(f"+deg({node}) = {incoming}")
        print(f"deg({node}) = {incoming + outcoming}\n")
    else:
        print(f"deg({node}) = {len(graph.adjacency_list[node])}\n")