import pygame
import genmaps
import random
import math
import entities
import render
import time

class Game(object):
    level = 1
    sector = genmaps.Map()
    player = entities.Player(id=0, level=1, location=sector.setPlayer())

    def __init__(self, level):
        self.level = level
        self.__FPS = 15
        self.__STEP = 64
        self.__WINDOW_HEIGHT = 1024
        self.__WINDOW_WEIGHT = 1024

    @property
    def getFps(self):
        return self.__FPS

    @property
    def getStep(self):
        return self.__STEP

    @property
    def getWindow(self):
        return self.__WINDOW_HEIGHT, self.__WINDOW_WEIGHT

    def renderView(self, god_mode):
        render.renderGame(sc, self.sector.maps, god_mode)
        # render.lightZone(sc)
        # sc.blit(lightZone, (0, 0))

    def restartLevel(self):
        countofrooms = random.randint(5, 10)
        self.sector.generateroom(countofrooms, True)
        countofchests = random.randint(2, countofrooms - math.floor(countofrooms / 2))
        self.sector.setChests(countofchests, self.level)
        self.sector.setLadder()
        countofmobs = random.randint(5, 5 + self.level)
        self.sector.setMobs(countofmobs, self.level)
        self.player.location = self.sector.setPlayer()

    def increaseLevel(self):
        self.level += 1
        self.sector.cleanUp()

    # def viewAllInfo(self):
    #     print(self.sector.mobs)
    #     print(self.player)
    #     # for i in self.sector.maps:
    #     #     print(i)
    #     # print(self.sector.center)

    def movePlayer(self, dx, dy):
        if self.sector.movePlayer(dx, dy):
            self.increaseLevel()
            self.restartLevel()

    def moveCurrentMob(self, mob, i, j):
        if self.sector.maps[i - 1][j] == '0' or self.sector.maps[i + 1][j] == '0' or self.sector.maps[i][
            j - 1] == '0' or self.sector.maps[i][j + 1] == '0':
            while True:
                di = random.randint(-1, 1)
                dj = random.randint(-1, 1)
                if di != 0 and dj != 0:
                    continue
                else:
                    if self.sector.maps[i + di][j + dj] == '1':
                        continue
                    else:
                        break
            self.sector.maps[i][j] = '0'
            mob.location[0] += di
            mob.location[1] += dj
            self.sector.maps[i + di][j + dj] = '3'

    def moveMobs(self):
        for i in range(0, len(self.sector.maps)):
            for j in range(0, len(self.sector.maps[i])):

                if self.sector.maps[i][j] == '3':
                    for mob in self.sector.mobs:
                        if mob.location == [i, j]:
                            self.moveCurrentMob(mob, i, j)


god_mode = True
game = Game(1)

pygame.init()
sc = pygame.display.set_mode(game.getWindow)
lightZone = pygame.display.set_mode(game.getWindow)
sc.blit(lightZone, (0, 0))
clock = pygame.time.Clock()
###########

game.renderView(god_mode)

###########
pygame.display.update()
while True:
    clock.tick(game.getFps)
    pygame.display.update()
    game.renderView(god_mode)
    game.moveMobs()
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_UP:
                game.movePlayer(-1, 0)
            elif i.key == pygame.K_DOWN:
                game.movePlayer(1, 0)
            elif i.key == pygame.K_LEFT:
                game.movePlayer(0, -1)
            elif i.key == pygame.K_RIGHT:
                game.movePlayer(0, 1)
            elif i.key == pygame.K_p:
                if not god_mode:
                    god_mode = True
                else:
                    god_mode = False
