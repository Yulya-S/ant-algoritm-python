import pygame
pygame.init()
from anthill import Anthill
anthi = Anthill()

sc = pygame.display.set_mode((800, 550))
sc.fill((255, 255, 255))

while 1:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
    anthi.draw(sc)
    pygame.display.update()