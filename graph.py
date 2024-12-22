import pygame
from random import randint

f1 = pygame.font.SysFont('Comic Sans MS', 12)
rangeX = 370
rangeY = 400

class Graph:
    def __init__(self, file_name: str = "", sep: str = " "):
        self.nodes: dict = {}
        if file_name != "":
            self.read_file(file_name, sep)

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

    def ORE(self):
        for i in self.nodes.values():
            neighbours = i.return_neighbours
            other_nodes = list(self.nodes.keys())
            other_nodes.remove(i.name)
            for l in neighbours:
                if l in other_nodes:
                    other_nodes.remove(l)
            for l in other_nodes:
                if self.nodes[l].neighbour_count + len(neighbours) >= len(self.nodes.keys()):
                    return True
        return False


    @property
    def return_nodes(self):
        return list(self.nodes.values())

    def add_node(self, name: str):
        self.nodes[name] = Node(name, (randint(0, rangeX), randint(0, rangeY)))
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

    def draw_lines(self, window, coord: tuple, line: list):
        for i in self.nodes.values():
            i.draw(window, coord, line, self.nodes)

    def draw(self, window, coord, path: list = []):
        self.draw_lines(window, coord, path)


class Node:
    def __init__(self, name: str, coord: tuple):
        self.name = name
        self.neighbours = {}
        self.coord = coord

    def copy(self):
        node_copy = Node(str(self.name), self.coord)
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

    def draw(self, window, coord: tuple, path: list = [], other_nodes: dict = {}):
        pygame.draw.circle(window, (0, 0, 0), (self.coord[0] + coord[0], self.coord[1] + coord[1]), 5, 1)
        text = f1.render(self.name, False, (0, 0, 0))
        window.blit(text, (self.coord[0] + coord[0] - 5, self.coord[1] + coord[1] - 20))
        index = -1 if self.name not in path else path.index(self.name)
        if index >= 0:
            node2 = index + 1 if len(path) > index + 1 else -1
            node2 = other_nodes[path[node2]]
            pygame.draw.line(window, (0, 0, 0), (self.coord[0] + coord[0], self.coord[1] + coord[1]),
                             (node2.coord[0] + coord[0], node2.coord[1] + coord[1]))
