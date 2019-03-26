import pygame
import genmaps
import random
import math


class Game(object):
    level = 1
    sector = genmaps.Map()

    def __init__(self, level):
        self.level = level
        self.__FPS = 10
        self.__STEP = 64
        self.__WINDOW_HEIGHT = 1024
        self.__WINDOW_WEIGHT = 800

    @property
    def getFps(self):
        return self.__FPS

    @property
    def getStep(self):
        return self.__STEP

    @property
    def getWindow(self):
        return self.__WINDOW_HEIGHT, self.__WINDOW_WEIGHT

    def renderView(self):
        pass

    def restartLevel(self):
        countofrooms = random.randint(5, 10)
        self.sector.generateroom(countofrooms, True)
        countofchests = random.randint(2, countofrooms - math.floor(countofrooms / 2))
        self.sector.setChests(countofchests, self.level)
        self.sector.setLadder()
        countofmobs = random.randint(5, countofrooms - math.floor(countofrooms / 2) + 10)
        self.sector.setMobs(countofmobs, self.level)

    def increaseLevel(self):
        self.level += 1
        self.sector.cleanUp()

    def viewAllInfo(self):
        for i in self.sector.maps:
            print(i)
        print(self.sector.center)


game = Game(1)

pygame.init()
pygame.display.set_mode(game.getWindow)
clock = pygame.time.Clock()
###########
game.restartLevel()
game.renderView()

###########
pygame.display.update()
while True:
    clock.tick(game.getFps)
    pygame.display.update()

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
