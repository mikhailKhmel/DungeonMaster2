import pygame
import genmaps
import random
import math
import entities
import render
import time

version = 'alpha 0.0.2'


class Game(object):
    level = 1
    sector = genmaps.Map()
    player = entities.Player(id=0, level=1, location=sector.setPlayer())

    def __init__(self, level):
        self.level = level
        self.__FPS = 15
        self.__STEP = 16
        self.__WINDOW_HEIGHT = 960
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

    def renderView(self, god_mode):
        render.renderGame(sc, self.sector.maps, god_mode, self.player)
        # render.lightZone(sc)
        # sc.blit(lightZone, (0, 0))

    def restartLevel(self):
        countofrooms = random.randint(5, 10)
        self.sector.generateroom(countofrooms, True)
        countofchests = random.randint(
            2, countofrooms - math.floor(countofrooms / 2))
        self.sector.setChests(countofchests, self.level)
        self.sector.setLadder()
        countofmobs = random.randint(5, 5 + self.level)
        self.sector.setMobs(countofmobs, self.level)
        self.player.location = self.sector.setPlayer()

    def increaseLevel(self):
        self.level += 1
        self.sector.cleanUp()

    def movePlayer(self, dx, dy):
        self.player.location = self.sector.movePlayer(dx, dy, self.player)
        if self.player.location == [0, 0]:
            self.increaseLevel()
            self.restartLevel()
        else:
            return

    def moveMobs(self):
        self.sector.moveMobs(self.player, sc)

    def __searchMob(self, di, dj):
        tmp = self.sector.mobs
        for i in range(0, len(tmp)):
            if tmp[i].location == [self.player.location[0] + di, self.player.location[1] + dj]:
                tmp[i].hp = tmp[i].hp - self.player.power
                render.attackMob(sc, tmp[i].location)
                if tmp[i].hp <= 0:
                    tmp.remove(tmp[i])
                    self.sector.maps[self.player.location[0] +
                                     di][self.player.location[1] + dj] = '0'
                self.sector.mobs = tmp
                return True
        return False

    def playerAttackMob(self):
        current_locationI = self.player.location[0]
        current_locationJ = self.player.location[1]
        if self.sector.maps[current_locationI + 1][current_locationJ] == '3':
            self.__searchMob(1, 0)
        elif self.sector.maps[current_locationI][current_locationJ + 1] == '3':
            self.__searchMob(0, 1)
        elif self.sector.maps[current_locationI - 1][current_locationJ] == '3':
            self.__searchMob(-1, 0)
        elif self.sector.maps[current_locationI][current_locationJ - 1] == '3':
            self.__searchMob(0, -1)


god_mode = False
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
    move_key = False
    # if game.player.hp<=0:
    #     break
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:

            if i.key == pygame.K_UP:
                game.movePlayer(-1, 0)
                move_key = True
            elif i.key == pygame.K_DOWN:
                game.movePlayer(1, 0)
                move_key = True
            elif i.key == pygame.K_LEFT:
                game.movePlayer(0, -1)
                move_key = True
            elif i.key == pygame.K_RIGHT:
                game.movePlayer(0, 1)
                move_key = True
            elif i.key == pygame.K_SPACE:
                game.playerAttackMob()
                move_key = True
            elif i.key == pygame.K_p:
                if not god_mode:
                    god_mode = True
                else:
                    god_mode = False
            if move_key:
                game.moveMobs()
