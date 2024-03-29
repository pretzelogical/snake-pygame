#!/usr/bin/env python3
import pygame
from pygame.math import Vector2
import random
from sys import argv
from collections import deque
pygame.init()

SCREEN_SIZE = 1024
# Pixel size of grid squares
GRID_SIZE = 32
TESTING = "test" in argv or "Test" in argv
# Colors
COL_BLACK = pygame.Color("black")
COL_RED = pygame.Color("red")
COL_DEBUG = pygame.Color("purple")
COL_SCORE = pygame.Color("#83d9c0")
# Font
FONT = pygame.font.SysFont("Cantarell", 32)


class Snake(pygame.Rect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = COL_BLACK
        self.lastHeading = pygame.K_UP
        if "pos" in kwargs:
            self.pos = kwargs["pos"]
        else:
            self.pos = Vector2(16, 16)

    @staticmethod
    def move(heading, fullSnake, foodEaten):
        """ Processes movement """
        headingMap = {
            pygame.K_LEFT: Vector2(-1, 0),
            pygame.K_RIGHT: Vector2(1, 0),
            pygame.K_UP: Vector2(0, -1),
            pygame.K_DOWN: Vector2(0, 1)
                       }
        heading = Snake.pickHeading(fullSnake[0], heading)
        if heading not in headingMap.keys():
            if TESTING:
                print(f"Invalid heading {pygame.key.name(heading)}")
            heading = fullSnake[0].lastHeading
        newPos = fullSnake[0].pos + headingMap[heading]
        if newPos.x < 0:
            newPos.x = GRID_SIZE - 1
        elif newPos.x >= GRID_SIZE:
            newPos.x = 0
        if newPos.y < 0:
            newPos.y = GRID_SIZE - 1
        elif newPos.y >= GRID_SIZE:
            newPos.y = 0

        fullSnake.appendleft(Snake(GRID_SIZE, GRID_SIZE, GRID_SIZE,
                                   GRID_SIZE, pos=newPos))

        if not foodEaten:
            fullSnake.pop()

        fullSnake[0].lastHeading = heading
        if TESTING:
            print(pygame.key.name(fullSnake[0].lastHeading))
            print(f"Pos: {fullSnake[0].pos}")
        return fullSnake

    @staticmethod
    def pickHeading(head, heading):
        """
        Picks the correct heading based on the
        last heading of the snake
        """
        if heading == pygame.K_LEFT and head.lastHeading == pygame.K_RIGHT:
            return pygame.K_RIGHT
        elif heading == pygame.K_RIGHT and head.lastHeading == pygame.K_LEFT:
            return pygame.K_LEFT
        elif heading == pygame.K_UP and head.lastHeading == pygame.K_DOWN:
            return pygame.K_DOWN
        elif heading == pygame.K_DOWN and head.lastHeading == pygame.K_UP:
            return pygame.K_UP
        return heading

    @staticmethod
    def newSnake(snake):
        """ Adds new snake block """
        pass
        # snake.append(Snake(GRID_SIZE, GRID_SIZE, GRID_SIZE,
        #                    GRID_SIZE, pos=snake[0].pos))
        # return snake

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
        if "pos" in kwargs:
            self.pos = kwargs["pos"]
        else:
            self.pos = Vector2(random.randint(0, GRID_SIZE - 1),
                               random.randint(0, GRID_SIZE - 1))

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, val):
        """ update screen position based on grid position """
        self.__pos = val
        self.x = self.__pos.x * GRID_SIZE
        self.y = self.__pos.y * GRID_SIZE

    @staticmethod
    def newFood(blocks):
        """Deletes food blocks and adds new food"""
        del [x for x in blocks if x.__class__.__name__ == "Food"][0]
        blocks = [x for x in blocks if x.__class__.__name__ != "Food"]
        food = Food(GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_SIZE)
        blocks.append(food)
        return blocks, food


class Debug(Food):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = COL_DEBUG
        if "pos" in kwargs:
            self.pos = kwargs.get("pos")
        else:
            self.pos = Vector2(0, 0)


def drawGameGrid(screen):
    for i in range(0, SCREEN_SIZE, GRID_SIZE):
        pygame.draw.line(screen, COL_BLACK, (i, 0), (i, SCREEN_SIZE))
        pygame.draw.line(screen, COL_BLACK, (0, i), (SCREEN_SIZE, i))


def drawBlocks(screen, blocks):
    """ Draws blocks """
    for block in blocks:
        pygame.draw.rect(screen, block.color, block)


def drawScore(screen, score):
    """ Draws score """
    scoreText = FONT.render(f"Score: {score}", True, COL_SCORE)
    scoreTextRect = scoreText.get_rect()
    scoreTextRect.center = (((SCREEN_SIZE // 3) * 3) - 100,
                            (SCREEN_SIZE // 4) - 200)
    screen.blit(scoreText, scoreTextRect)


def drawGameOver(screen):
    """ Draws Game Over """
    gameOverText = FONT.render("Game Over", True, COL_RED)
    gameOverTextRect = gameOverText.get_rect()
    gameOverTextRect.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 2)
    screen.blit(gameOverText, gameOverTextRect)


def testDraw(screen, frames):
    """ Draws testing info """
    frameText = FONT.render(f"{frames}", True, COL_RED)
    frameTextRect = frameText.get_rect()
    frameTextRect.center = (SCREEN_SIZE // 2, SCREEN_SIZE // 4)
    screen.blit(frameText, frameTextRect)


def initSnakeBlocks(num_children):
    snake = deque()
    snakeHead = Snake(GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_SIZE, head=True)
    snake.append(snakeHead)
    offset = Vector2(16, 17)
    for i in range(1, num_children + 1):
        parent = snake[i - 1]
        newPart = Snake(GRID_SIZE, GRID_SIZE,
                        GRID_SIZE, GRID_SIZE, pos=offset)
        snake.append(newPart)
        parent.child = snake[i]
        offset = offset.copy()
        offset += Vector2(0, 1)
    return snake


def doCollisions(blocks, food, score):
    positions = [x.pos for x in blocks]
    foodEaten = False
    gameOver = False
    for pos in positions:
        if foodEaten:
            break
        if positions.count(pos) != 1:
            collided = [x for x in blocks if x.pos == pos]
            if TESTING:
                print(f'match {pos}')
            if "Food" in [x.__class__.__name__ for x in collided]:
                if TESTING:
                    print("Food eaten")
                blocks, food = Food.newFood(blocks)
                score += 1
                foodEaten = True
            else:
                if TESTING:
                    print(f"Snake died at {pos}")
                    blocks.append(Debug(GRID_SIZE, GRID_SIZE,
                                        GRID_SIZE, GRID_SIZE, pos=pos))
                gameOver = True

    return blocks, food, score, foodEaten, gameOver


def main():
    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    snake = initSnakeBlocks(3)
    food = Food(GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_SIZE)
    debug = Debug(GRID_SIZE, GRID_SIZE, GRID_SIZE, GRID_SIZE)
    blocks = list(snake) + [food] + [debug]
    running = True
    heading = pygame.K_UP
    score = 0
    foodEaten = False
    gameOver = False
    if TESTING:
        print("Testing mode")
        print(blocks)
        frameCount = 0

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
        blocks = list(snake) + [food]
        Snake.move(heading, snake, foodEaten)
        blocks, food, score, \
            foodEaten, gameOver = doCollisions(blocks, food, score)

        # Drawing logic
        screen.fill((255, 255, 255))
        drawGameGrid(screen)
        drawBlocks(screen, blocks)
        drawScore(screen, score)
        if gameOver:
            drawGameOver(screen)
            running = False
        if TESTING:
            frameCount += 1
            testDraw(screen, frameCount)
            print([[x.__class__.__name__, x.pos] for x in blocks])

        pygame.display.flip()
        clock.tick(4)

    if gameOver:
        pygame.time.wait(2000)

    pygame.quit()


main()
