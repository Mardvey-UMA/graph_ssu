# 3. Для каждой вершины графа вывести её степень.
from Graph_cotainer import Graph, graph_path
import os
os.chdir(graph_path)
graph = Graph.console_input()
graph.print_degrees()