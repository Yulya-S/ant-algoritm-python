from graph import Graph
import pygame

f1 = pygame.font.SysFont('Comic Sans MS', 24)

class Anthill:
    def __init__(self):
        self.__recreate()

    def __recreate(self):
        self.read_conf_file()
        self.graph: Graph = Graph(self.__file_name)
        if not self.graph.ORE():
            quit()
        self.graph2: Graph = self.graph.copy()
        self.greate_path: list = []
        self.best_length: int = -1
        self.ant_count: int = 0

    def read_conf_file(self):
        try:
            with open("conf.txt", "r") as file:
                data = file.read().split("\n")
                self.__file_name = data[0]
                self.__sep = data[1]
                self.alfa = float(data[2])
                self.beta = float(data[3])
                self.evaluation_rate = float(data[4])
                self.fix_count = int(data[5])
                self.max_ant_count = int(data[6])
        except:
            with open("conf.txt", "w") as file:
                file.write("graph.txt\n,\n3.0\n2.0\n0.1\n100\n10000")
            self.read_conf_file()

    def draw(self, window):
        self.graph.draw(window, (10, 10), ["1", "31", "8"])
        self.graph2.draw(window, (410, 10), ["1", "31", "8"])
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

class Ant:
    def __init__(self):
        pass