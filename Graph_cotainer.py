import json
from collections import defaultdict, deque
from functools import singledispatchmethod
import os
import copy

graph_path = "P:\\graph\\graph_ssu\\graph_files"


class Node:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value


class Graph:
    def __init__(self, directed=False, weighted=False):
        self.directed = directed
        self.weighted = weighted
        self.adjacency_list = defaultdict(set)
        self.node_info = {}
        self.cycles = []
        if self.weighted:
            self.weights = defaultdict(lambda: float('inf'))
        else:
            self.weights = None

    def copy(self):
        new_graph = Graph(directed=self.directed, weighted=self.weighted)
        new_graph.adjacency_list = copy.deepcopy(self.adjacency_list)
        new_graph.node_info = copy.deepcopy(self.node_info)
        if self.weighted:
            new_graph.weights = copy.deepcopy(self.weights)
        return new_graph

    def __str__(self):
        result = ""
        directed = ""
        wheighted = ""
        if self.directed:
            directed += "ориентированный"
        if self.weighted:
            wheighted = "взвешенный"
        if not self.weighted and not self.directed:
            result += f"Тип графа: простой граф\n"
        else:
            result += f"Тип графа: {wheighted, directed}\n"

        for node, neighbors in self.adjacency_list.items():
            if True:  # len(neighbors) != 0:
                result += f"{node} -> {', '.join(neighbors)}\n"
        if self.weighted:
            result += "\nВес ребер:\n"
            for (start, end), weight in self.weights.items():
                result += f"{start} -> {end} : {weight}\n"

        return result

    # Задача 3: Метод для вывода степени каждой вершины
    def print_degrees(self):
        for node in self.adjacency_list.keys():
            if self.directed:
                outgoing = len(self.adjacency_list[node])
                incoming = len([n for n, neighbors in self.adjacency_list.items() if node in neighbors])
                print(f"-deg({node}) = {outgoing}")
                print(f"+deg({node}) = {incoming}")
                print(f"deg({node}) = {incoming + outgoing}\n")
            else:
                print(f"deg({node}) = {len(self.adjacency_list[node])}\n")

    # Задача 13: Метод для поиска вершин, одновременно входящих и исходящих для данной вершины
    def find_bidirectional_vertices(self, node):
        if node not in self.adjacency_list:
            raise ValueError(f"Вершина {node} не найдена в графе")

        outgoing_vertices = self.adjacency_list[node]
        incoming_vertices = {v for v, neighbors in self.adjacency_list.items() if node in neighbors}
        result = outgoing_vertices & incoming_vertices

        if result:
            print(f"Вершины, которые одновременно заходят и выходят для {node}: {', '.join(result)}")
        else:
            print(f"Для вершины {node} нет одновременно входящих и выходящих вершин.")

    # Задача 18: Метод для удаления вершин с нечётными степенями
    def remove_odd_degree_vertices(self):
        new_graph = self.copy()
        deleted_nodes = []

        print("Исходный граф:")
        print(self)

        for node in list(new_graph.adjacency_list.keys()):
            outgoing = len(new_graph.adjacency_list[node])
            incoming = len([n for n, neighbors in new_graph.adjacency_list.items() if node in neighbors])
            degree = outgoing + incoming if self.directed else len(new_graph.adjacency_list[node])

            if degree % 2 != 0 and degree != 0:
                deleted_nodes.append(node)

        for node in deleted_nodes:
            new_graph.del_node(node)

        print("Граф после удаления вершин с нечётными степенями:")
        print(new_graph)
        return new_graph

    def dfs(self, start_node):
        if start_node not in self.adjacency_list:
            raise ValueError(f"Вершина {start_node} не найдена в графе")

        visited = set()  # посещенные вершины
        traversal_order = []  # путь обхода

        def dfs_recursive(node):
            visited.add(node)
            traversal_order.append(node)

            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(start_node)

        return traversal_order, len(traversal_order)

    def bfs(self, start_node):
        if start_node not in self.adjacency_list:
            raise ValueError(f"Вершина {start_node} не найдена в графе")

        visited = set([start_node])  # посещенные вершины
        queue = deque([start_node])  # очередь
        traversal_order = []  # пройденный путь

        while queue:
            node = queue.popleft()
            traversal_order.append(node)

            for neighbor in self.adjacency_list[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return traversal_order, len(traversal_order)

    # 23 Проверить, можно ли из орграфа удалить какую-либо вершину так, чтобы получилось дерево.
    def is_tree_after_removal(self):
        for node in list(self.adjacency_list.keys()):
            new_graph = self.copy()
            new_graph.del_node(node)

            if self._is_connected(new_graph) and not self._has_cycle(new_graph):
                print(f"Граф может стать деревом после удаления вершины: {node}")
                return True

        print("Невозможно превратить граф в дерево удалением одной вершины.")
        return False

    def _is_connected(self, graph):
        if not graph.adjacency_list:
            return True

        start_node = next(iter(graph.adjacency_list))
        traversal_order, num_nodes_reached = graph.bfs(start_node)

        return num_nodes_reached == len(graph.adjacency_list)

    def _has_cycle(self, graph):
        visited = set()

        def dfs_with_cycle_detection(node, parent):
            visited.add(node)
            for neighbor in graph.adjacency_list[node]:
                if neighbor not in visited:
                    if dfs_with_cycle_detection(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            return False

        for node in graph.adjacency_list:
            if node not in visited:
                if dfs_with_cycle_detection(node, None):
                    return True
        return False

    @singledispatchmethod
    def add_node(self, node: Node):
        if node.name in self.adjacency_list:
            print(f"Узел {node.name} уже есть в графе")
        else:
            self.adjacency_list[node.name] = set()
            self.node_info[node.name] = node.value

    # Добавление узла по кортежу (имя, значение)
    @add_node.register
    def _(self, node_info: tuple):
        name, value = node_info
        if name in self.adjacency_list:
            print(f"Узел {name} уже есть в графе")
        else:
            self.adjacency_list[name] = set()
            self.node_info[name] = value

    # Добавление узла по имени с значение по умолчанию
    @add_node.register(str)
    def _(self, node_name: str):
        if node_name in self.adjacency_list:
            print(f"Узел {node_name} уже есть в графе")
        else:
            self.add_node(Node(node_name, None))

    # Добавление ребра дуги по кортежу имя значение
    @singledispatchmethod
    def add_connect(self, first_node_info: tuple, second_node_info: tuple, weight=None):
        first_name, first_value = first_node_info
        second_name, second_value = second_node_info

        is_first_exist = first_name in self.adjacency_list
        is_second_exist = second_name in self.adjacency_list

        is_agree = False

        if is_first_exist and is_second_exist:
            is_agree = True
        elif is_first_exist and not is_second_exist:
            flag = input("Второй узел не найден, добавить?, [y(да)/n(нет)]")
            if flag == 'y':
                is_agree = True
                self.add_node(second_node_info)
            elif flag == 'n':
                print("Операция остановлена")
        elif not is_first_exist and is_second_exist:
            flag = input("Первый узел не найден, добавить?, [y(да)/n(нет)]")
            if flag == 'y':
                is_agree = True
                self.add_node(first_node_info)
            elif flag == 'n':
                print("Операция остановлена")
        elif not is_first_exist and not is_second_exist:
            flag = input("Оба узла не найдены, добавить?, [y(да)/n(нет)]")
            if flag == 'y':
                is_agree = True
                self.add_node(second_node_info)
                self.add_node(first_node_info)
            elif flag == 'n':
                print("Операция остановлена")

        if is_agree:
            self.adjacency_list[first_name].add(second_name)

            if not self.directed:
                self.adjacency_list[second_name].add(first_name)

            if self.weighted:
                if weight is None:
                    raise ValueError("Укажите вес для взвешенного графа")
                self.weights[(first_name, second_name)] = weight
                if not self.directed:
                    self.weights[(second_name, first_name)] = weight

    # Перегрузка добавления через класс Node
    @add_connect.register
    def _(self, first_node: Node, second_node: Node, weight=None):
        self.add_connect((first_node.name, first_node.value), (second_node.name, second_node.value), weight)

    # Перегрузка добавления через имя со значениями по умолчанию
    @add_connect.register
    def _(self, first_node_name: str, second_node_name: str, weight=None):
        self.add_connect((first_node_name, None), (second_node_name, None), weight)

    # Поиск по имени
    @singledispatchmethod
    def find_node(self, name: str):
        if name not in self.adjacency_list:
            return f"Узел с именем {name} не найден"
        return self._node_info(name)

    # Поиск по значению
    @find_node.register(int)
    def _(self, value: int):
        found_nodes = [name for name, node_value in self.node_info.items() if node_value == value]
        if not found_nodes:
            return f"Узлы со значением {value} не найдены"
        result = ""
        for node in found_nodes:
            result += self._node_info(node)
        return result

    # Поиск по кортежу (имя, значение)
    @find_node.register(tuple)
    def _(self, node_info: tuple):
        name, value = node_info
        if name not in self.adjacency_list:
            return f"Узел с именем {name} не найден"
        if self.node_info.get(name) != value:
            return f"Узел с именем {name}, но с другим значением ({self.node_info[name]})"
        return self._node_info(name)

    # Информация об узле
    def _node_info(self, name: str):
        info = f"Узел {name} со значением {self.node_info[name]}\n"
        if self.directed:
            outgoing = ', '.join(self.adjacency_list[name])
            incoming = ', '.join(n for n, neighbors in self.adjacency_list.items() if name in neighbors)
            info += f"Выходящие узлы: {outgoing or 'нет'}\n"
            info += f"Входящие узлы: {incoming or 'нет'}\n"
        else:
            neighbors = ', '.join(self.adjacency_list[name])
            info += f"Смежные узлы: {neighbors or 'нет'}\n"
        return info

    # Удаление узла по имени узла
    def del_node(self, name: str):
        if name in self.adjacency_list:
            self.adjacency_list.pop(name)
            self.node_info.pop(name)
            for k in self.adjacency_list.keys():
                self.adjacency_list[k].discard(name)
            if self.weighted:
                temp = []
                for k in self.weights.keys():
                    if name in k:
                        temp.append(k)
                for t in temp:
                    self.weights.pop(t)
        else:
            print(f'Узел {name} не найден')

    # Удаление ребра/дуги по имени
    def del_connect(self, name1: str, name2: str):
        if name1 in self.adjacency_list and name2 in self.adjacency_list:
            if self.directed:
                if name2 in self.adjacency_list[name1]:
                    self.adjacency_list[name1].discard(name2)
                else:
                    print(f"Такого ребра не существует")
            else:
                if name2 in self.adjacency_list[name1] or name1 in self.adjacency_list[name2]:
                    self.adjacency_list[name1].discard(name2)
                    self.adjacency_list[name2].discard(name1)
                else:
                    print(f"Такой дуги не существует")

        else:
            print("Один из улов не существует")

    # Сохранение графа в .json файл
    def save_to_file(self, file_path):
        graph_data = {
            "type": ["directed"] if self.directed else ["undirected"],
            "nodes": [{"name": node, "value": self.node_info[node]} for node in self.node_info],
            "edges": [{"from": n1, "to": n2, "weight": self.weights[(n1, n2)] if self.weighted else None}
                      for n1 in self.adjacency_list for n2 in self.adjacency_list[n1]]
        }

        with open(file_path, 'w') as file:
            json.dump(graph_data, file, indent=4)
        print(f"Граф сохранен в {file_path}")

    # Загрузка графа через файл
    @classmethod
    def load_from_file(cls, file_path):
        with open(file_path, 'r') as file:
            graph_data = json.load(file)

        directed = "directed" in graph_data["type"]
        weighted = any(edge.get("weight") is not None for edge in graph_data["edges"])

        graph = cls(directed=directed, weighted=weighted)

        for node in graph_data["nodes"]:
            graph.add_node((node["name"], node["value"]))

        for edge in graph_data["edges"]:
            weight = edge.get("weight") if weighted else None
            graph.add_connect(edge["from"], edge["to"], weight)

        print(f"Граф загружен из {file_path}")
        return graph

    # Статический метод для консольного интерфейса ввода графа
    @staticmethod
    def console_input():
        load_from_file = input("Загрузить граф из файла? (y/n): ").strip().lower() == 'y'
        if load_from_file:
            files = [f for f in os.listdir() if f.endswith('.json')]
            if files:
                print("Доступные файлы в текущей директории:")
                for idx, file in enumerate(files):
                    print(f"{idx + 1}. {file}")

            file_selection = input("Введите номер файла или полный путь: ").strip()
            if file_selection.isdigit():
                file_idx = int(file_selection) - 1
                if 0 <= file_idx < len(files):
                    file_path = files[file_idx]
                else:
                    raise ValueError("Неверный номер файла")
            else:
                file_path = file_selection

            return Graph.load_from_file(file_path)

        directed = input("Граф ориентированный? (y/n): ").strip().lower() == 'y'
        weighted = input("Граф взвешенный? (y/n): ").strip().lower() == 'y'
        graph = Graph(directed=directed, weighted=weighted)

        while True:
            node_name = input("Введите узел (или оставьте пустым для завершения): ").strip()
            if not node_name:
                break
            value = input(f"Значение узла {node_name} (по умолчанию None): ") or None
            graph.add_node((node_name, value))

        while True:
            first_node = input("Введите первый узел для ребра (или оставьте пустым для завершения): ").strip()
            if not first_node:
                break
            second_node = input("Введите второй узел для ребра: ").strip()
            weight = None
            if graph.weighted:
                weight = float(input("Вес ребра: "))
            graph.add_connect(first_node, second_node, weight)

        return graph

    # консольное меню отдельно
    def console_menu(self):
        while True:
            print("\n1 - Сохранить граф в файл")
            print("2 - Добавить узел")
            print("3 - Добавить ребро")
            print("4 - Удалить узел")
            print("5 - Удалить ребро")
            print("6 - Просмотреть информацию о графе")
            print("7 - Выйти")
            choice = input("Выберите действие: ").strip()

            if choice == '1':  # Сохранение графа в файл
                file_path = input("Введите имя файла для сохранения (.json): ").strip()
                self.save_to_file(file_path)
            elif choice == '2':  # Добавление узла
                node_name = input("Введите имя узла: ").strip()
                value = int(input(f"Значение узла {node_name} (по умолчанию None): ") or None)
                self.add_node((node_name, value))
            elif choice == '3':  # Добавление ребра/дуги
                first_node = input("Введите первый узел: ").strip()
                second_node = input("Введите второй узел: ").strip()
                weight = None
                if self.weighted:
                    weight = float(input("Вес ребра: "))
                self.add_connect(first_node, second_node, weight)
            elif choice == '4':  # Удаление узла
                node_name = input("Введите имя узла для удаления: ").strip()
                self.del_node(node_name)
            elif choice == '5':  # Удаление ребра/Дуги
                first_node_name = input("Введите имя первого узла: ").strip()
                second_node_name = input("Введите имя второго узла: ").strip()
                self.del_connect(first_node_name, second_node_name)
            elif choice == '6':  # Вывод информации о графе
                print(self)
            elif choice == '7':
                print("Выход из программы")
                break
            else:
                print("Неверный выбор, попробуйте снова")
