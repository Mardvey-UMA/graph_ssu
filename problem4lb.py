# 18.Построить граф, полученный однократным удалением вершин с нечётными степенями.
# Добавить все в общий класс + добавить что-то там вумное
from Graph_cotainer import Graph, graph_path
import os
os.chdir(graph_path)
graph1 = Graph.console_input()
graph = graph1.copy()
print("До удаления:")
print(graph)
deleted = []
for node in graph.adjacency_list.keys():
    outcoming = len(graph.adjacency_list[node])
    incoming = len([n for n, neighbors in graph.adjacency_list.items() if node in neighbors])
    if (outcoming + incoming) % 2:
        print(f"Удален узел {node}")
        deleted.append(node)
for node in deleted:
    graph.del_node(node)

print("После удаления:")
print(graph)