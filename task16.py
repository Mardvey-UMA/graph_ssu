from Graph_cotainer import Graph


graph = Graph(directed=False, weighted=True)

graph.add_node('A')
graph.add_node('B')
graph.add_node('C')
graph.add_node('D')

graph.add_connect('A', 'B', 1)
graph.add_connect('B', 'C', 2)
graph.add_connect('A', 'C', 4)
graph.add_connect('C', 'D', 1)
graph.add_connect('B', 'D', 5)

distances, paths = graph.find_shortest_paths_to_node('D')
if distances:
    for vertex, distance in distances.items():
        print(f"Путь до {vertex}:")
        path = paths[vertex]
        path = list(reversed(path))
        print(f"Путь: {' -> '.join(path)}")
        print(f"Длина пути: {distance}")