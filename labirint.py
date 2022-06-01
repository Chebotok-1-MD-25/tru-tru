import pygame
from random import choice
width, height = 750, 750
tile = 50

cols = (width // tile +1) // 2
rows = (height // tile +1) // 2

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Лабиринт")
clock = pygame.time.Clock()

class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right':}
while True:
    screen.fill(pygame.color('black'))

    for event in pygame.event.get():
        if event.type == pygame.quit:
            exit()


