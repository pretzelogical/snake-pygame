#!/usr/bin/env python3
import pygame

SCREEN_SIZE = 1024
# Pixel size of grid squares
GRID_SIZE = 32


def createGameField():
    """ Returns a cols x rows list"""
    rows = cols = SCREEN_SIZE // GRID_SIZE
    return [[None for i in range(cols)] for j in range(rows)]


def drawGameGrid(screen):
    for i in range(0, SCREEN_SIZE, GRID_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (i, 0), (i, SCREEN_SIZE))
        pygame.draw.line(screen, (0, 0, 0), (0, i), (SCREEN_SIZE, i))


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Snake")
    # gameField = createGameField(32)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    

        screen.fill((255, 255, 255))
        drawGameGrid(screen)
        pygame.display.flip()

        clock.tick(60)
    pygame.quit()

main()
