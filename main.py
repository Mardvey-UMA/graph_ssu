import os

from Graph_cotainer import Graph, graph_path

os.chdir(graph_path)
graph = Graph.console_input()
graph.console_menu()
