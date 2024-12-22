from graph import Graph

gr = Graph("graph.txt", " ")
gr2 = gr.copy()

import pygame
pygame.init()

sc = pygame.display.set_mode((800, 600))
sc.fill((255, 255, 255))

# f1 = pygame.font.Font(None, 36)
# text1 = f1.render('Hello Привет', 1, (180, 0, 0))
#
#
# sc.blit(text1, (10, 50))
#
#
# pygame.display.update()

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()

    gr.draw(sc, (10, 10), ["1", "31", "8"])
    gr2.draw(sc, (410, 10), ["1", "31", "8"])
    pygame.draw.line(sc, (0, 0, 0), (400, 0), (400, 420))
    pygame.draw.line(sc, (0, 0, 0), (0, 420), (800, 420))
    pygame.display.update()