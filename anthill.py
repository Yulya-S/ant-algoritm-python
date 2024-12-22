from graph import Graph
import pygame
import random

f1 = pygame.font.SysFont('Comic Sans MS', 24)


class Anthill:
    def __init__(self):
        self.__recreate()

    def __recreate(self):
        with open("result.txt", "w") as _:
            pass
        self.read_conf_file()
        self.graph: Graph = Graph(self.__file_name, self.__sep)
        if not self.graph.ORE():
            print("В выбранном графе отсутствует Гамильтонов цикл")
            quit()
        self.greate_path: list = []
        self.best_length: int = -1
        self.__best_length_count: int = 0
        self.ant_count: int = 0
        self.__ants: list = []

    def read_conf_file(self):
        try:
            with open("conf.txt", "r") as file:
                data = file.read().split("\n")
                self.__file_name = data[0]
                self.__sep = data[1]
                if self.__sep == "":
                    self.__sep = " "
                self.alpha = float(data[2])
                self.beta = float(data[3])
                self.evaluation_rate = float(data[4])
                self.fix_count = int(data[5])
                self.max_ant_count = int(data[6])
                self.__spawn_chance = float(data[7])
                self.__ants_in_pack = int(data[8])
        except:
            with open("conf.txt", "w") as file:
                file.write("graph.txt\n \n3.0\n2.0\n0.1\n100\n10000\n1\n10")
            self.read_conf_file()

    def __pheramone_recalculation(self, ant_path: list, trail_summ: int):
        pass

    def step(self):
        while len(self.__ants) != self.__ants_in_pack:
            self.__ants.append(Ant(self.graph.copy(), self.ant_count + 1, self.alpha, self.beta))
            self.ant_count += 1
        for i in range(len(self.__ants)):
            if self.__ants[i].step():
                if self.__ants[i].end_trail:
                    self.graph = self.__ants[i].graph
                    if self.best_length > self.__ants[i].trail_summ or self.best_length == -1:
                        self.best_length = self.__ants[i].trail_summ
                        self.greate_path = self.__ants[i].path
                    elif self.best_length == self.__ants[i].trail_summ:
                        self.__best_length_count += 1
                    else:
                        self.__best_length_count = 0
                    with open("result.txt", "a") as file:
                        file.write(
                            f"{self.ant_count} {self.__ants[i].trail_summ} {self.__ants[i].sum_of_probabilities}\n")
                    self.ant_count += 1
                self.__ants[i] = Ant(self.graph.copy(), self.ant_count + 1, self.alpha, self.beta)

    def draw(self, window):
        self.graph.draw(window, (10, 10), self.greate_path)
        if len(self.__ants) > 0:
            self.__ants[0].draw(window, (410, 10))
        pygame.draw.line(window, (0, 0, 0), (400, 0), (400, 450))
        pygame.draw.line(window, (0, 0, 0), (0, 420), (800, 420))
        pygame.draw.line(window, (0, 0, 0), (0, 450), (800, 450))
        text = f1.render("Лучший путь", True, (0, 0, 0))
        window.blit(text, (20, 415))
        text = f1.render("Текущий путь", True, (0, 0, 0))
        window.blit(text, (420, 415))
        text = f1.render(f"Лучший найденный путь: {' '.join(self.greate_path)}", True, (0, 0, 0))
        window.blit(text, (20, 450))
        text = f1.render(f"Длина лучшего пути: {self.best_length}", True, (0, 0, 0))
        window.blit(text, (20, 480))
        text = f1.render(f"Количество муравьев: {self.ant_count}", True, (0, 0, 0))
        window.blit(text, (20, 510))
        text = f1.render(f"Число фиксация: {self.__best_length_count}", True, (0, 0, 0))
        window.blit(text, (20, 540))


class Ant:
    def __init__(self, graph: Graph, name: int, alpha: float, beta: float):
        self.name: str = str(name)
        self.graph: Graph = graph
        self.path: list = []
        self.trail_summ: int = 0
        self.end_trail: bool = False
        self.impasse: bool = False
        self.sum_of_probabilities: float = 1.
        self.__alpha = alpha
        self.__beta = beta

    @property
    def __last_node(self):
        return self.graph.nodes[self.path[-1]]

    def denominator(self):
        summ = 0.0
        for i in self.__last_node.return_neighbours:
            if i not in self.path:
                summ += self.__calculate_formula(self.__last_node.neighbours[i])
        return summ

    def __calculate_formula(self, node_value: list):
        return (node_value[1] ** self.__alpha) * ((1 / node_value[0]) ** self.__beta)

    def ant_in_impasse(self):
        for i in list(self.graph.nodes[self.path[-1]].neighbours.keys()):
            if i not in self.path:
                return False
        return True

    def step(self):
        if len(self.path) == 0:
            self.path.append(random.choice(list(self.graph.nodes.keys())))
        denominator = self.denominator()
        summ = 0
        rand = random.random()
        for i in self.__last_node.return_neighbours:
            if i not in self.path:
                probability = self.__calculate_formula(self.__last_node.neighbours[i]) / denominator
                summ += probability
                if rand <= summ:
                    self.trail_summ += self.__last_node.neighbours[i][0]
                    self.path.append(i)
                    self.sum_of_probabilities *= probability
                    return False
        if len(self.path) == len(self.graph.nodes.keys()) and self.path[0] in self.__last_node.return_neighbours:
            self.trail_summ += self.__last_node.neighbours[self.path[0]][0]
            self.path.append(self.path[0])
            self.end_trail = True
        else:
            self.impasse = True
        return True

    def draw(self, window, coord: tuple):
        self.graph.draw(window, coord, self.path)
        text = f1.render(self.name, False, (255, 100, 100))
        window.blit(text, coord)
