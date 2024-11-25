from Graph_cotainer import Graph

graph = Graph.load_from_file(r"P:\graph\graph_ssu\graph_files\floyd_test5.json")
paths, shortest_length = graph.task21("A", "B")

paths, shortest_length = graph.task21("F", "G")

paths, shortest_length = graph.task21("A", "D")


