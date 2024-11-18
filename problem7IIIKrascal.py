# Дан взвешенный неориентированный граф из N вершин и M ребер.
# Требуется найти в нем каркас минимального веса.
# Алгоритм, который необходимо реализовать для решения задачи
# (Прима или Краскала), выдает преподаватель.
from Graph_cotainer import Graph, graph_path
import os
os.chdir(graph_path)
graph = Graph.console_input()
print(graph)
graph.find_minimal_spanning_tree_kruskal()
