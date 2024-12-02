from Graph_cotainer import Graph


graph = Graph(weighted=True)
graph.add_node('A')
graph.add_node('B')
graph.add_node('C')
graph.add_node('D')
graph.add_node('E')
graph.add_node('H')
graph.add_node('G')
graph.add_node('F')
graph.add_node('X')

graph.add_connect('A', 'B', 4)
graph.add_connect('B', 'F', 4)

graph.add_connect('A', 'C', 2)
graph.add_connect('C', 'D', 2)
graph.add_connect('D', 'F', 4)

graph.add_connect('A', 'E', 2)
graph.add_connect('E', 'H', 2)
graph.add_connect('H', 'G', 2)
graph.add_connect('G', 'F', 2)

graph.add_connect('A', 'X', 8)
graph.add_connect('X', 'F', 8)

graph.add_connect('A', 'F', 8)


print("Граф:")
print(graph)

k_paths = graph.find_k_shortest_paths('A', 'F', 4)

for i, path in enumerate(k_paths, 1):
    print(f"Путь {i}: {' -> '.join(path)}")