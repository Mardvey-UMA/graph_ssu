# 13. Вывести те вершины орграфа, которые являются одновременно заходящими и выходящими для заданной вершины.
from Graph_cotainer import Graph, graph_path
import os
os.chdir(graph_path)
graph = Graph.console_input()
node = input("Введите имя вершины: ").strip()

if node not in graph.adjacency_list:
    raise ValueError(f"Вершина {node} не найдена в графе")

outgoing_vertices = graph.adjacency_list[node]

incoming_vertices = {v for v, neighbors in graph.adjacency_list.items() if node in neighbors}

result = outgoing_vertices & incoming_vertices

if result:
    print(f"Вершины, которые одновременно заходят и выходят для {node}: {', '.join(result)}")
else:
    print(f"Для вершины {node} нет одновременно входящих и выходящих вершин.")