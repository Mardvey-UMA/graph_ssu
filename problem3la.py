# 13. Вывести те вершины орграфа, которые являются одновременно заходящими и выходящими для заданной вершины.
from Graph_cotainer import Graph, graph_path
import os
os.chdir(graph_path)
graph = Graph.console_input()
while True:
    node = input("Введите имя вершины (или оставтье пустым для завершения): ").strip()
    if node:
        graph.find_bidirectional_vertices(node)
    else:
        break