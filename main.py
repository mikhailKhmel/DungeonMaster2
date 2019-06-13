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

    def initPlayer(self):
        self.player.hp = 6
        self.player.armor = 0
        self.player.armor_lvl=0
        self.player.weapon_lvl=0
        self.player.power=1
        self.player.inventory=[]
        self.player.location=self.sector.setPlayer()

    def restartLevel(self):
        sc.fill((0,0,0))
        self.sector.cleanUp()
        self.sector.__init__()
        # countofrooms = random.randint(5, 10)
        # self.sector.generateroom(countofrooms, True)
        # countofchests = random.randint(
        #     2, countofrooms - math.floor(countofrooms / 2))
        # self.sector.setChests(countofchests, self.level)
        # self.sector.setLadder()
        # countofmobs = random.randint(5, 5 + self.level)
        # self.sector.setMobs(countofmobs, self.level)
        self.initPlayer()

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

    def renderMenu(self, sc, pos, InProccess):
        #sc.fill((0, 0, 0))
        f = pygame.font.SysFont('CourerNew', 32)
        if InProccess:
            menu = ['Return', 'Restart', 'Exit']
        else:
            menu = ['Start', 'Exit']
        y = 0
        for i in range(0, len(menu)):
            if i == pos:
                t = f.render(menu[i], 0, (255, 255, 0))
            else:
                t = f.render(menu[i], 0, (255, 255, 255))
            sc.blit(t, (0, y))
            y += 32
        return menu

    def menu(self, InProccess, sc):
        menu = True
        pos = 0
        while menu:
            pygame.display.update()
            clock.tick(game.getFps)

            list_menu = game.renderMenu(sc, pos, InProccess)
            length_menu=len(list_menu)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN:
                        if pos+1 > length_menu-1:
                            pass
                        else:
                            pos += 1
                    elif e.key == pygame.K_UP:
                        if pos-1 < 0:
                            pass
                        else:
                            pos -= 1
                    elif e.key == pygame.K_RETURN:
                        if list_menu[pos] == 'Start' or list_menu[pos] == 'Return':
                            menu = False
                        elif list_menu[pos] == 'Restart':
                            self.restartLevel()
                            menu = False
                        elif list_menu[pos] == 'Exit':
                            quit()


god_mode = False
game = Game(1)

pygame.init()
sc = pygame.display.set_mode(game.getWindow)
lightZone = pygame.display.set_mode(game.getWindow)
sc.blit(lightZone, (0, 0))
clock = pygame.time.Clock()
###########

game.menu(False,sc)

game.renderView(god_mode)

###########
pygame.display.update()
while True:
    clock.tick(game.getFps)
    pygame.display.update()
    game.renderView(god_mode)
    move_key = False
    if game.player.hp <= 0:
        sc.fill((255, 0, 0))
        f = pygame.font.SysFont('CourerNew', 72)
        gameover_text = f.render("GAME OVER", 0, (0, 0, 0))
        sc.blit(gameover_text, (100, 100))
        pygame.display.update()
        time.sleep(2)
        game.restartLevel()
        game.menu(False,sc)
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
            elif i.key==pygame.K_ESCAPE:
                game.menu(True,sc)
            if move_key:
                game.moveMobs()
