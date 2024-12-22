import pygame
pygame.init()
from anthill import Anthill
anthi = Anthill()

sc = pygame.display.set_mode((800, 600))

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        if i.type == pygame.KEYDOWN and i.key == pygame.K_UP:
            anthi.step()
    sc.fill((255, 255, 255))
    #anthi.step()
    anthi.draw(sc)
    pygame.display.update()