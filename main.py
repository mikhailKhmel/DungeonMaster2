import pygame
import genmaps
import random
import math
import entities
import render
import time

version = 'alpha 1.1.5'


class Game(object):
    level = 1
    sector = genmaps.Map(level=level)
    player = entities.Player(id=0, location=sector.setPlayer())

    def __init__(self, level):
        self.level = level
        self.__FPS = 20
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
        render.renderGame(sc, self.sector.maps, god_mode, self.player, self.level, len(self.sector.mobs))

    def initPlayer(self):
        self.player.hp = 10
        self.player.armor = 0
        self.player.armor_lvl=0
        self.player.weapon_lvl=0
        self.player.power=1
        self.player.inventory=['','','','','','']
        self.player.location=self.sector.setPlayer()

    def restartLevel(self, new_player):
        sc.fill((0,0,0))
        self.sector.__init__(level=self.level)
        if new_player:
            self.initPlayer()
        else:
            self.player.location=self.sector.setPlayer()


    def increaseLevel(self):
        global zero_mobs
        zero_mobs = False
        self.level += 1

    def movePlayer(self, dx, dy):
        self.player.location = self.sector.movePlayer(dx, dy, self.player)
        if self.player.location == [0, 0]:
            self.increaseLevel()
            self.restartLevel(False)
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
        f = pygame.font.Font('src/Minecraftia.ttf', 48)
        if InProccess:
            menu = ['return', 'restart', 'exit']
        else:
            menu = ['start', 'exit']
        y = 72
        for i in range(0, len(menu)):
            if i == pos:
                t = f.render(menu[i], 0, (255, 255, 0))
            else:
                t = f.render(menu[i], 0, (255, 255, 255))
            sc.blit(t, (0, y))
            y += 72
        return menu

    def inv_mode(self):
        mode = True
        pos=0
        while mode:
            pygame.display.update()
            clock.tick(self.getFps)
            render.renderInfoAboutPlayer(sc,self.player,self.level,len(self.sector.mobs))
            render.renderInv(sc,self.player,mode,pos)
            
            for e in pygame.event.get():
                if e.type==pygame.KEYDOWN:
                    if e.key==pygame.K_LEFT:
                        if pos!=0:
                            pos-=1
                    elif e.key==pygame.K_RIGHT:
                        if pos!=5:
                            pos+=1
                    elif e.key==pygame.K_UP:
                        if pos not in [0,1,2]:
                            pos-=3
                    elif e.key==pygame.K_DOWN:
                        if pos not in [3,4,5]:
                            pos+=3
                    
                    elif e.key==pygame.K_e:
                        mode=False
                    elif e.key==pygame.K_q:
                        self.player.inventory[pos] = ''
                    elif e.key==pygame.K_SPACE:
                        selected_item = self.player.inventory[pos]
                        if selected_item == '':
                            continue
                        elif selected_item == 'potion':
                            if self.player.hp == 10:
                                continue
                            else:
                                self.player.hp += 1
                                self.player.inventory[pos] = ''
                        elif selected_item[:len(selected_item)-1] == 'disk_lvl':
                            if int(selected_item[len(selected_item)-1]) <= self.player.weapon_lvl:
                                continue
                            else:
                                self.player.weapon_lvl = int(selected_item[len(selected_item)-1])
                                self.player.power = 1 + self.player.weapon_lvl
                                self.player.inventory[pos] = ''
                        elif selected_item[:len(selected_item)-1] == 'armor_lvl':
                            if int(selected_item[len(selected_item)-1]) <= self.player.armor_lvl:
                                continue
                            else:
                                self.player.armor_lvl = int(selected_item[len(selected_item)-1])
                                self.player.inventory[pos] = ''


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
                    elif e.key == pygame.K_ESCAPE:
                        if list_menu[0] == 'start':
                            quit()
                        else:
                            menu = False
                    elif e.key == pygame.K_RETURN:
                        if list_menu[pos] == 'start' or list_menu[pos] == 'return':
                            menu = False
                        elif list_menu[pos] == 'restart':
                            self.restartLevel(True)
                            menu = False
                        elif list_menu[pos] == 'exit':
                            quit()
    
    def checkChest(self):
        x = self.player.location[0]
        y = self.player.location[1]
        if self.sector.maps[x-1][y] == '5':
            return [x-1,y] 
        elif self.sector.maps[x+1][y] == '5':
            return [x+1,y]
        elif self.sector.maps[x][y-1] == '5':
            return [x,y-1]
        elif self.sector.maps[x][y+1] == '5':
            return [x,y+1]
        else:
            return []

    def addToInvFromChest(self,item):
        pos=0
        for i in self.player.inventory:
            if i == '':
                self.player.inventory[pos] = item
                return
            else:
                pos+=1

    def openChest(self):
        loc = self.checkChest()
        if loc != []:
            r = random.randint(1,3)
            if r in [1,2]:
                self.addToInvFromChest('potion')
                self.sector.maps[loc[0]][loc[1]] = '0'
                return
            else:
                r = random.randint(1,2)

                if r==1:
                    item = 'disk_lvl' + str(self.player.weapon_lvl+1)
                    self.addToInvFromChest(item)
                    self.sector.maps[loc[0]][loc[1]] = '0'
                    return
                else:
                    
                    item = 'armor_lvl' + str(self.player.weapon_lvl+1)
                    self.addToInvFromChest(item)
                    self.sector.maps[loc[0]][loc[1]] = '0'
                    return
        else:
            return
        
    def printLog(self):
        print('LVL=',self.level)
        print('MAP')
        for i in self.sector.maps:
            print (i)
        print('MOBS')
        for i in self.sector.mobs:
            print('id=',i.id)
            print('location=',i.location)
            print('power=',i.power)
            print('hp=',i.hp)
            print('\n')
        print('ROOMS')
        for i in self.sector.rooms:
            print([i.x1,i.x2,i.y1,i.y2])
        print('CENTERS')
        print(self.sector.center)
        print('CHESTS')
        for i in self.sector.chests:
            print(i.location)
        print('\nPLAYER LOG')
        print(self.player.location)
        print(self.player.hp)
        print(self.player.power)
        print(self.player.armor_lvl)
        print(self.player.weapon_lvl)
        print(self.player.inventory)



god_mode = False
zero_mobs = False
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
mob_clk=0
move_clk=0
while True:
    fps=game.getFps
    clock.tick(fps)
    pygame.display.update()
    game.renderView(god_mode)
    move_key = False
    if game.player.hp <= 0:
        sc.fill((255, 0, 0))
        f = pygame.font.Font('src/Minecraftia.ttf', 48)
        gameover_text = f.render("GAME OVER", 0, (0, 0, 0))
        sc.blit(gameover_text, (500, 500))
        pygame.display.update()
        time.sleep(2)
        game.level=1
        game.restartLevel(True)
        game.menu(False,sc)
    
    keys = pygame.key.get_pressed()
    delay = 2
    if keys[pygame.K_UP]:
        if move_clk==delay:
            game.movePlayer(-1, 0)
            move_clk=0
        else:
            move_clk+=1
    elif keys[pygame.K_DOWN]:
        if move_clk==delay:
            game.movePlayer(1, 0)
            move_clk=0
        else:
            move_clk+=1
    elif keys[pygame.K_RIGHT]:
        if move_clk==delay:
            game.movePlayer(0, 1)
            move_clk=0
        else:
            move_clk+=1
    elif keys[pygame.K_LEFT]:
        if move_clk==delay:
            game.movePlayer(0,-1)
            move_clk=0
        else:
            move_clk+=1

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            game.printLog()
            # if i.key == pygame.K_UP:
            #     game.movePlayer(-1, 0)
            #     move_key = True
            # elif i.key == pygame.K_DOWN:
            #     game.movePlayer(1, 0)
            #     move_key = True
            # elif i.key == pygame.K_LEFT:
            #     game.movePlayer(0, -1)
            #     move_key = True
            # elif i.key == pygame.K_RIGHT:
            #     game.movePlayer(0, 1)
            #     move_key = True
            if i.key == pygame.K_SPACE:
                game.playerAttackMob()
                move_key = True
            elif i.key == pygame.K_p:
                if not god_mode:
                    god_mode = True
                else:
                    god_mode = False
            elif i.key == pygame.K_r:
                game.openChest()
            elif i.key==pygame.K_ESCAPE:
                game.menu(True,sc)
            elif i.key==pygame.K_e:
                game.inv_mode()
                
    if mob_clk==int(fps/3):
        game.moveMobs()
        mob_clk=0
    else:
        mob_clk+=1
    
    
    if len(game.sector.mobs)==0 and not zero_mobs:
        game.addToInvFromChest('potion')
        zero_mobs = True
