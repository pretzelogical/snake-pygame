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
        self.lastHeading = pygame.K_UP
        self.head = kwargs.get("head", False)
        self.parent = kwargs.get("parent", None)
        self.child = kwargs.get("child", None)
        self.old_pos = self.pos.copy()
        if not self.head and not self.parent:
            raise ValueError("Snake must have parent if not head")

    def move(self, heading, gameField):
        """ Processes movement """
        if not self.head:
            self.update()
            return
        headingMap = {
            pygame.K_LEFT: Vector2(-1, 0),
            pygame.K_RIGHT: Vector2(1, 0),
            pygame.K_UP: Vector2(0, -1),
            pygame.K_DOWN: Vector2(0, 1)
                   }
        heading = self.pickHeading(heading)
        if heading in headingMap:
            self.pos += headingMap[heading]
        self.lastHeading = heading
        if TESTING:
            print(pygame.key.name(heading))
            print(f"Pos: {self.pos}")
        return

    def pickHeading(self, heading):
        """
        Picks the correct heading based on the
        last heading of the snake
        """
        if heading == pygame.K_LEFT and self.lastHeading == pygame.K_RIGHT:
            return pygame.K_RIGHT
        elif heading == pygame.K_RIGHT and self.lastHeading == pygame.K_LEFT:
            return pygame.K_LEFT
        elif heading == pygame.K_UP and self.lastHeading == pygame.K_DOWN:
            return pygame.K_DOWN
        elif heading == pygame.K_DOWN and self.lastHeading == pygame.K_UP:
            return pygame.K_UP
        return heading

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, val):
        """ update screen position based on grid position """
        self.__pos = val
        self.x = self.__pos.x * GRID_SIZE
        self.y = self.__pos.y * GRID_SIZE


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


def initSnakeBlocks(num_children):
    snake = []
    snakeHead = Snake(GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_SIZE, head=True)
    snake.append(snakeHead)
    offset = Vector2(16, 16)
    for i in range(1, num_children + 1):
        parent = snake[i - 1]
        newPart = Snake(GRID_SIZE, GRID_SIZE,
                        GRID_SIZE, GRID_SIZE, parent=parent)
        newPart.pos = offset
        snake.append(newPart)
        parent.child = snake[i]
        offset += Vector2(0, 1)
    return snake


def main():
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Snake")
    if TESTING:
        print("Testing mode")
        frameCount = 0
    gameField = createGameField()
    clock = pygame.time.Clock()
    snake = initSnakeBlocks(3)
    food = Food(0, 0, GRID_SIZE, GRID_SIZE)
    blocks = snake + [food]
    if TESTING:
        print(blocks)
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
        for s in snake:
            if s.head:
                s.move(heading, gameField)

        # Drawing logic
        screen.fill((255, 255, 255))
        drawGameGrid(screen)
        drawBlocks(screen, blocks)
        if TESTING:
            frameCount += 1
            print(snake[1].parent.old_pos)
            print(snake[1].old_pos)
            testDraw(screen, frameCount)

        pygame.display.flip()
        clock.tick(2)
    pygame.quit()


main()
