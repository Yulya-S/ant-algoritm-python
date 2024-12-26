import random
import time
from graph import Graph
import sys


class Hamilton_bilder_big_graf:
    def __init__(self, graph: Graph):
        self.__graph = graph.copy()
        self.__min_edge_count: int = -1
        self.__greate_queue: list = []
        self.__base: dict = {}
        if len(self.__graph.nodes.keys()) > 800:
            sys.setrecursionlimit(10000)
        self.__max_chain = -1
        self.__chein = []
        self.__timer = time.time()

    def __checking_result(self, queue: list = [], edge_count: int = 0):
        if edge_count < self.__min_edge_count or self.__min_edge_count == -1:
            self.__min_edge_count = edge_count
            self.__greate_queue = queue.copy()
            self.__timer = time.time()
            print(f"Найден путь с добавлением: {self.__min_edge_count + 1} ребер")

    def __find_max_chein(self, queue: list, start_pos: int = 0):
        for l in range(start_pos + 1, len(queue)):
            if queue[start_pos + 1] in list(self.__graph.nodes[queue[start_pos]].neighbours.keys()):
                self.__find_max_chein(queue.copy(), start_pos + 1)
            elif self.__max_chain == -1 or start_pos > self.__max_chain:
                self.__max_chain = start_pos
                self.__chein = queue[:start_pos]
            queue.append(queue.pop(start_pos + 1))

    def process(self, queue: list = [], start_pos: int = 0, edge_count: int = 0):
        if time.time() - self.__timer > 30:
            return

        if self.__min_edge_count != -1 and edge_count >= self.__min_edge_count:
            return

        if queue == []:
            queue = list(self.__graph.nodes.keys())
            self.__find_max_chein(queue)
            if self.__max_chain != -1:
                for i in self.__chein:
                    if i in queue:
                        queue.remove(i)
                queue = self.__chein + queue
            start_pos = self.__max_chain

        if start_pos + 1 >= len(queue):
            if queue[0] not in self.__graph.nodes[queue[-1]].return_neighbours:
                edge_count += 1
            self.__checking_result(queue, edge_count)
            return

        new_queue = queue.copy()
        new_queue = new_queue[start_pos:]
        self.__max_chain = -1
        self.__chein = []
        self.__find_max_chein(new_queue)
        start_pos_copy = start_pos
        if self.__max_chain > 0:
            for i in self.__chein:
                if i in queue:
                    queue.remove(i)
            queue = self.__chein + queue
            start_pos_copy += self.__max_chain - 1
            self.process(queue.copy(), start_pos_copy, edge_count)

        if start_pos == 0:
            return

        for l in range(start_pos + 1, len(queue)):
            if queue[start_pos + 1] not in list(self.__graph.nodes[queue[start_pos]].neighbours.keys()):
                new_queue = queue.copy()
                new_queue = new_queue[start_pos + 1:]
                self.__max_chain = -1
                self.__chein = []
                self.__find_max_chein(new_queue)
                start_pos_copy = start_pos + 1
                if self.__max_chain > 0:
                    for i in self.__chein:
                        if i in queue:
                            queue.remove(i)
                    queue = self.__chein + queue
                    start_pos_copy += self.__max_chain - 1
                self.process(queue.copy(), start_pos_copy, edge_count + 1)
                if start_pos + 1 == start_pos_copy:
                    return
                if time.time() - self.__timer > 30:
                    break
            queue.append(queue.pop(start_pos + 1))

    def build(self):
        if self.__min_edge_count == -1:
            print("Достроить Гамильтонов цикл не вышло!")
            quit()
        count = 0
        for i in range(len(self.__greate_queue)):
            l = i + 1
            if l >= len(self.__greate_queue):
                l = 0
            if self.__greate_queue[l] not in self.__graph.nodes[self.__greate_queue[i]].return_neighbours:
                self.__graph.add_edge(self.__greate_queue[i], self.__greate_queue[l], 1)
                count += 1
        print(f"\nДля создания Гамильтонова цикла было добавлено: {count} ребер")
        self.__graph.write_graf("hamilton_graf.txt")
        with open("cicle.txt", "w") as file:
            file.write(", ".join(self.__greate_queue))
        print("Гамильтонов путь был сохранен в файле: cicle.txt")
        return self.__graph

class Hamilton_bilder_small_graf:
    def __init__(self, graph: Graph):
        self.__graph = graph.copy()
        self.__min_edge_count: int = -1
        self.__greate_queue: list = []
        self.__base: dict = {}
        if len(self.__graph.nodes.keys()) > 800:
            sys.setrecursionlimit(10000)
        self.__tails = {}
        self.__tails_results = {}
        self.__couples = []
        self.__generations = 0


    def __checking_result(self, queue: list = [], edge_count: int = 0):
        if edge_count < self.__min_edge_count or self.__min_edge_count == -1:
            self.__min_edge_count = edge_count
            self.__greate_queue = queue.copy()
            print(f"Найден путь с добавлением: {self.__min_edge_count} ребер")

    def process(self, queue: list = [], start_pos: int = 0, edge_count: int = 0):
        if queue == []:
            queue = list(self.__graph.nodes.keys())
        if self.__min_edge_count != -1 and edge_count >= self.__min_edge_count:
            return
        if start_pos + 1 >= len(queue):
            if queue[0] not in self.__graph.nodes[queue[-1]].return_neighbours:
                edge_count += 1
            self.__checking_result(queue, edge_count)


        for l in range(start_pos + 1, len(queue)):
            if queue[start_pos + 1] in list(self.__graph.nodes[queue[start_pos]].neighbours.keys()):
                self.process(queue.copy(), start_pos + 1, edge_count)
            else:
                self.process(queue.copy(), start_pos + 1, edge_count + 1)
            queue.append(queue.pop(start_pos + 1))

    def build(self):
        if self.__min_edge_count == -1:
            print("Достроить Гамильтонов цикл не вышло!")
            quit()
        for i in range(len(self.__greate_queue)):
            l = i + 1
            if l >= len(self.__greate_queue):
                l = 0
            if self.__greate_queue[l] not in self.__graph.nodes[self.__greate_queue[i]].return_neighbours:
                self.__graph.add_edge(self.__greate_queue[i], self.__greate_queue[l], 1)
        print(f"\nДля создания Гамильтонова цикла было добавлено: {self.__min_edge_count} ребер")
        self.__graph.write_graf("hamilton_graf.txt")
        return self.__graph
