class Graph:
    def __init__(self):
        self.nodes: dict = {}
        self.read_file()

    # чтение данных из файла
    def read_file(self, file_name: str = "graph.txt"):
        pass

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
        if node1_name == node2_name:
            raise Exception("У двух выбранных нод одинаковое имя")
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