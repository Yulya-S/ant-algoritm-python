class Graph:
    def __init__(self, file_name: str = "", sep: str = " "):
        if file_name != "":
            self.read_file(file_name, sep)
        else:
            self.nodes: dict = {}

    def copy(self):
        graph_copy = Graph()
        for i in list(self.nodes.keys()):
            graph_copy.nodes[i] = self.nodes[i].copy()
        return graph_copy

    # чтение данных из файла
    def read_file(self, file_name: str = "graph.txt", sep: str = " "):
        self.nodes: dict = {}
        with open(file_name) as file:
            for i in file:
                i = i.split(sep)
                if len(i) >= 3:
                    self.add_edge(i[0], i[1], int(i[2]))

    @property
    def return_nodes(self):
        return list(self.nodes.values())

    def add_node(self, name: str):
        self.nodes[name] = Node(name)
        print(f"Добавлена нода {name}")

    def remove_node(self, name: str):
        for i in self.return_nodes:
            i.remove_neighbour(name)
        self.nodes.pop(name)
        print(f"Удалена нода {name}")

    def add_edge(self, node1_name: str, node2_name: str, price: int, pheromones: float = 0.1):
        if node1_name not in list(self.nodes.keys()):
            self.add_node(node1_name)
        if node2_name not in list(self.nodes.keys()):
            self.add_node(node2_name)
        self.nodes[node1_name].add_neighbour(node2_name, price, pheromones)
        print(f"Добавлена связь между нодами {node1_name} и {node2_name}")

    def remove_edge(self, node1_name: str, node2_name: str):
        if node1_name == node2_name:
            raise Exception("У двух выбранных нод одинаковое имя")
        self.nodes[node1_name].remove_neighbour(node2_name)
        print(f"Удалена связь между нодами {node1_name} и {node2_name}")


class Node:
    def __init__(self, name: str):
        self.name = name
        self.neighbours = {}

    def copy(self):
        node_copy = Node(str(self.name))
        for i in list(self.neighbours.keys()):
            node_copy.neighbours[i] = self.neighbours[i].copy()
        return node_copy

    @property
    def neighbour_count(self):
        return len(self.neighbours.keys())

    @property
    def return_neighbours(self):
        return list(self.neighbours.keys())

    def add_neighbour(self, name: str, price: int, pheromones: float):
        if name not in self.return_neighbours:
            self.neighbours[name] = [price, pheromones]
        else:
            print(f"Сосед с именем: {name} уже существует!")

    def remove_neighbour(self, name: str):
        self.neighbours.pop(name)