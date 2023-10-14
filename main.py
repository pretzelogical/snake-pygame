#!/usr/bin/env python3
import pygame

SCREEN_SIZE = 1024
# Pixel size of grid squares
GRID_SIZE = 32
# Colors
COL_BLACK = pygame.Color("black")
COL_RED = pygame.Color("red")

class Snake(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = COL_BLACK
        
class Food(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = COL_RED

def createGameField():
    """ Returns a cols x rows list"""
    rows = cols = SCREEN_SIZE // GRID_SIZE
    return [[None for i in range(cols)] for j in range(rows)]


def drawGameGrid(screen):
    for i in range(0, SCREEN_SIZE, GRID_SIZE):
        pygame.draw.line(screen, COL_BLACK, (i, 0), (i, SCREEN_SIZE))
        pygame.draw.line(screen, COL_BLACK, (0, i), (SCREEN_SIZE, i))

def drawBlocks(screen, blocks):
    """ Draws blocks """
    for block in blocks:
        pygame.draw.rect(screen, block.color, block)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Snake")
    gameField = createGameField()
    clock = pygame.time.Clock()
    snake = Snake(GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_SIZE)
    food = Food(0, 0, GRID_SIZE, GRID_SIZE)
    blocks = [snake, food]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    

        screen.fill((255, 255, 255))
        drawGameGrid(screen)
        drawBlocks(screen, blocks)
        pygame.display.flip()

        clock.tick(60)
    pygame.quit()

main()
