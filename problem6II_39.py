# 39 Для каждой вершины найти кратчайшее
# (по числу рёбер) расстояние от неё до ближайшей из заданного множества вершин.
from Graph_cotainer import Graph, graph_path
import os

os.chdir(graph_path)
paths = ["gr8.json", "gr9.json", "gr10.json", "gr11.json", "gr12.json", "gr13.json", "gr14.json"]
target_vertices = {"A", "C"}  # Заданное множество вершин для поиска кратчайшего расстояния

for path in paths:
    g = Graph.load_from_file(path)
    print(g)

    distances = g.find_shortest_distance(target_vertices)
    print("Кратчайшие расстояния до ближайшей вершины из множества", target_vertices)
    for vertex, distance in distances.items():
        print(f"Вершина {vertex}: расстояние = {distance}")
