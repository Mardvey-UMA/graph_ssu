# 23 * Проверить, можно ли из орграфа удалить какую-либо вершину так, чтобы получилось дерево.
from Graph_cotainer import Graph, graph_path
import os
os.chdir(graph_path)
paths = ["gr1.json", "gr2.json", "gr3.json", "gr4.json", "gr5.json", "gr6.json", "gr7.json"]
for path in paths:
    g = Graph.load_from_file(path)
    print(g)
    g.is_tree_after_delete_node()
