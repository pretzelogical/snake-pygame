#!/usr/bin/env python3
import pygame
from pygame.math import Vector2
from sys import argv
pygame.init()

SCREEN_SIZE = 1024
# Pixel size of grid squares
GRID_SIZE = 32
TESTING = "test" in argv or "Test" in argv
# Colors
COL_BLACK = pygame.Color("black")
COL_RED = pygame.Color("red")
# Font
FONT = pygame.font.SysFont("Cantarell", 32)


class Snake(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = COL_BLACK
        self.pos = Vector2(16, 16)
        self.x = self.pos.x * GRID_SIZE
        self.y = self.pos.y * GRID_SIZE

    def move(self, heading, gameField):
        """ Processes movement """
        headingMap = {
            pygame.K_LEFT: Vector2(-1, 0),
            pygame.K_RIGHT: Vector2(1, 0),
            pygame.K_UP: Vector2(0, -1),
            pygame.K_DOWN: Vector2(0, 1)
                   }
        if heading in headingMap:
            self.pos += headingMap[heading]
        self.x = self.pos.x * GRID_SIZE
        self.y = self.pos.y * GRID_SIZE
        if TESTING:
            print(pygame.key.name(heading))
            print(self.pos)

    def perimCheck(self, gameField):
        """ Checks if snake is colliding with another block"""
        raise NotImplementedError("perimCheck not implemented")


class Food(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = COL_RED
        self.pos = Vector2(10, 13)


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


def testDraw(screen, frames):
    """ Draws testing info """
    frameText = FONT.render(f"{frames}", True, COL_RED)
    frameTextRect = frameText.get_rect()
    frameTextRect.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 4)
    screen.blit(frameText, frameTextRect)


def main():
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Snake")
    if TESTING:
        print("Testing mode")
        frameCount = 0
    gameField = createGameField()
    clock = pygame.time.Clock()
    snake = Snake(GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_SIZE)
    food = Food(0, 0, GRID_SIZE, GRID_SIZE)
    blocks = [snake, food]
    running = True
    heading = pygame.K_UP

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if TESTING:
                    print(pygame.key.name(event.key))
                heading = event.key

        # Game logic
        snake.move(heading, gameField)

        # Drawing logic
        screen.fill((255, 255, 255))
        drawGameGrid(screen)
        drawBlocks(screen, blocks)
        if TESTING:
            frameCount += 1
            testDraw(screen, frameCount)

        pygame.display.flip()
        clock.tick(2)
    pygame.quit()


main()
