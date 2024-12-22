import pygame
pygame.init()
from anthill import Anthill
anthi = Anthill()

sc = pygame.display.set_mode((800, 600))
stop = False
step = False

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.KEYDOWN and i.key == pygame.K_RIGHT:
            step = True
        if i.type == pygame.KEYDOWN and i.key == pygame.K_SPACE:
            stop = not stop

    sc.fill((255, 255, 255))
    if not stop or step:
        if anthi.step():
            exit()
            break
        step = False
    anthi.draw(sc)
    pygame.display.update()