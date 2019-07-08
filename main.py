import random
import math
import time
import sqlite3

import pygame

import genmaps
import entities
import render


VERSION = 'alpha 1.3'

conn = sqlite3.connect('stats.db')
cursor = conn.cursor()



class Game(object):
    level = 1
    sector = genmaps.Map(level=level)
    player = entities.Player(id=0, location=sector.setPlayer(), view_location=[32*5,32*5])
    username = ''
    def __init__(self, level):
        self.level = level
        self.__FPS = 20
        self.__STEP = 16
        self.__WINDOW_HEIGHT = 960
        self.__WINDOW_WEIGHT = 800

        # if not cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';"):
        #     sql = """ 
        #     CREATE TABLE users (username text, highest_level integer)
        #     """
        #     cursor.execute(sql)

    @property
    def getFps(self):
        return self.__FPS

    @property
    def getStep(self):
        return self.__STEP

    @property
    def getWindow(self):
        return self.__WINDOW_HEIGHT, self.__WINDOW_WEIGHT

    def renderView(self, god_mode, first_start):
        render.renderGame(sc, self.sector.maps, god_mode, self.player, self.level, len(self.sector.mobs), first_start)

    def initPlayer(self):
        self.player.hp = 10
        self.player.armor = 0
        self.player.armor_lvl=0
        self.player.weapon_lvl=0
        self.player.power=1
        self.player.inventory=['','','','','','']
        self.player.location=self.sector.setPlayer()
        self.player.view_location=[32*5,32*5]

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
                render.attackMob(sc, [self.player.view_location[1] + di*32, self.player.view_location[0] + dj*32])
                if tmp[i].hp <= 0:
                    tmp.remove(tmp[i])
                    self.sector.maps[self.player.location[0] +
                                     di][self.player.location[1] + dj] = '0'
                self.sector.mobs = tmp
                return
                

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


    def enter_name(self,sc):
        size = 16
        name = []
        curr_index = 0
        
        while True:
            pygame.display.update()
            clock.tick(self.getFps)

            if len(name)>=24:
                continue

            f = pygame.font.Font('src/Minecraftia.ttf', size)

            t = f.render('Enter your name', 0, (255,255,255))
            sc.blit(t,(0,0))
            x=0
            for i in name:
                t = f.render(i,0,(255,255,255))
                x+=size
                sc.blit(t,(x,size*3))
            pass
            
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        curr_index -= 1
                        del name[curr_index]
                        sc.fill((0,0,0))
                        break
                    elif e.key == pygame.K_a: 
                        name += 'a'
                    elif e.key == pygame.K_b: 
                        name += 'b'
                    elif e.key == pygame.K_c: 
                        name += 'c'
                    elif e.key == pygame.K_d: 
                        name += 'd'
                    elif e.key == pygame.K_e: 
                        name += 'e'
                    elif e.key == pygame.K_f: 
                        name += 'f'
                    elif e.key == pygame.K_g: 
                        name += 'g'
                    elif e.key == pygame.K_h: 
                        name += 'h'
                    elif e.key == pygame.K_i: 
                        name += 'i'
                    elif e.key == pygame.K_j: 
                        name += 'j'
                    elif e.key == pygame.K_k: 
                        name += 'k'
                    elif e.key == pygame.K_l: 
                        name += 'l'
                    elif e.key == pygame.K_m: 
                        name += 'm'
                    elif e.key == pygame.K_n: 
                        name += 'n'
                    elif e.key == pygame.K_o: 
                        name += 'o'
                    elif e.key == pygame.K_p: 
                        name += 'p'
                    elif e.key == pygame.K_q: 
                        name += 'q'
                    elif e.key == pygame.K_r: 
                        name += 'r'
                    elif e.key == pygame.K_s: 
                        name += 's'
                    elif e.key == pygame.K_t: 
                        name += 's'
                    elif e.key == pygame.K_u: 
                        name += 'u'
                    elif e.key == pygame.K_v: 
                        name += 'v'
                    elif e.key == pygame.K_w: 
                        name += 'w'
                    elif e.key == pygame.K_x: 
                        name += 'x'
                    elif e.key == pygame.K_y: 
                        name += 'y'
                    elif e.key == pygame.K_z: 
                        name += 'z'

                    elif e.key == pygame.K_0: 
                        name += '0'
                    elif e.key == pygame.K_1: 
                        name += '1'
                    elif e.key == pygame.K_2: 
                        name += '2'
                    elif e.key == pygame.K_3: 
                        name += '3'
                    elif e.key == pygame.K_4: 
                        name += '4'
                    elif e.key == pygame.K_5: 
                        name += '5'
                    elif e.key == pygame.K_6: 
                        name += '6'
                    elif e.key == pygame.K_7: 
                        name += '7'
                    elif e.key == pygame.K_8: 
                        name += '8'
                    elif e.key == pygame.K_9: 
                        name += '9'
                    
                    elif e.key == pygame.K_SLASH:
                        name+='/'
                    elif e.key == pygame.K_EXCLAIM:
                        name+='!'
                    elif e.key == pygame.K_QUOTEDBL:
                        name+='"'
                    elif e.key == pygame.K_HASH:
                        name+='#'
                    elif e.key == pygame.K_DOLLAR:
                        name+='$'
                    elif e.key == pygame.K_AMPERSAND:
                        name+='&'
                    elif e.key == pygame.K_LEFTPAREN:
                        name+='('
                    elif e.key == pygame.K_RIGHTPAREN:
                        name+=')'


                    elif e.key == pygame.K_RETURN:
                        sql = "select username from users where username='" + ''.join(name) + "'"
                        if cursor.execute(sql):
                            tmp_username = cursor.fetchone()
                            if tmp_username != None:
                                self.username = ''.join(name)
                            else:
                                sql = 'insert into users (username, highest_level) values ("'+''.join(name)+'", 0)'
                                cursor.execute(sql)
                                conn.commit()
                                self.username = ''.join(name)
                        sc.fill((0,0,0))
                        return
                   # sc.fill((0,0,0))
                    curr_index += 1
                    
    def renderMenu(self, sc, pos, InProccess):
        #sc.fill((0, 0, 0))
        f = pygame.font.Font('src/Minecraftia.ttf', 48)
        if InProccess:
            menu = ['return', 'restart', 'exit']
            y = 80
        else:
            menu = ['start','stats', 'exit']
            y = 180
        for i in range(0, len(menu)):
            if i == pos:
                t = f.render(menu[i], 0, (255, 255, 0))
            else:
                t = f.render(menu[i], 0, (255, 255, 255))
            sc.blit(t, (0, y))
            y += 72
        return menu

    def show_stats(self):
        sc.fill((0,0,0))
        while True:
            
            pygame.display.update()
            clock.tick(self.getFps)

            sql = 'select * from users'
            result = cursor.execute(sql)
            
            f = pygame.font.Font('src/Minecraftia.ttf', 48)
            t = f.render('username      highest_level',0,(255,255,255))
            sc.blit(t,(0,0))
            t = f.render('==========================',0,(255,255,255))
            sc.blit(t,(0,48))
            c=2
            for row in result:
                t = f.render(str(row[0]), 0, (255,255,255))
                sc.blit(t,(0,48*c))
                t = f.render(str(row[1]), 0, (255,255,255))
                sc.blit(t,(48*10,48*c))
                c+=1
            c+=1
            t = f.render('BACK',0,(255,255,0))
            sc.blit(t,(0,48*c))
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return
            


    def menu(self, InProccess, sc, firstStart):
        
        if firstStart:
            self.enter_name(sc)

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
                        elif list_menu[pos] == 'stats':
                            self.show_stats()
                            sc.fill((0,0,0))
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

game.menu(False,sc, True)

game.renderView(god_mode, True)

###########
pygame.display.update()
mob_clk=0
move_clk=0
while True:
    fps=game.getFps
    clock.tick(fps)
    pygame.display.update()
    game.renderView(god_mode, False)
    move_key = False
    if game.player.hp <= 0:
        sql = 'select highest_level from users where username="'+str(game.username)+'"'
        cursor.execute(sql)
        result = cursor.fetchone()
        if int(result[0])<game.level:
            sql = 'update users set highest_level='+str(game.level)+' where username="'+str(game.username)+'"'
            cursor.execute(sql)
            conn.commit()

        sc.fill((255, 0, 0))
        f = pygame.font.Font('src/Minecraftia.ttf', 48)
        gameover_text = f.render("GAME OVER", 0, (0, 0, 0))
        sc.blit(gameover_text, (250, 250))
        pygame.display.update()
        time.sleep(2)
        game.level=1
        game.restartLevel(True)
        game.menu(False,sc, False)
    
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
           #game.printLog()
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
                game.menu(True,sc, False)
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
