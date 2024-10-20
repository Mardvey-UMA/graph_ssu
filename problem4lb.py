# 18.Построить граф, полученный однократным удалением вершин с нечётными степенями.
# Добавить все в общий класс + добавить что-то там вумное
from Graph_cotainer import Graph, graph_path
import os
os.chdir(graph_path)
graph = Graph().console_input()
graph.remove_odd_degree_vertices()
