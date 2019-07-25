import random
import sqlite3
import time

import pygame

import entities
import genmaps
import render

VERSION = 'alpha 1.4.1'

conn = sqlite3.connect('stats.db')
cursor = conn.cursor()


class Game(object):
    level = 1
    sector = genmaps.Map(level=level)
    sector_view = [[]]
    player = entities.Player(
        id=0, location=sector.setPlayer(), view_location=[32 * 5, 32 * 5])
    username = ''
    control_mode = 1  # 0 - only keyboard. 1 - keyboard and mouse
    god_mode = False
    zero_mobs = False

    clock = pygame.time.Clock()
    mob_clk = 0
    move_clk = 0
    killed_mobs = 0

    def __init__(self, level):

        self.level = level
        self.FPS = 20
        self.__WINDOW_HEIGHT = 960
        self.__WINDOW_WEIGHT = 800
        self.sector_view_append()
        self.god_mode = False
        self.zero_mobs = False
        pygame.init()
        self.sc = pygame.display.set_mode(self.getWindow)
        self.lightZone = pygame.display.set_mode(self.getWindow)
        self.sc.blit(self.lightZone, (0, 0))
        self.menu(False, True)
        self.renderView()
        self.mob_clk = 0
        self.move_clk = 0
        self.killed_mobs = 0
        # self.cycle()

    def sector_view_append(self):
        self.sector_view = [[]]
        for i in range(0, len(self.sector.maps)):
            for j in range(0, len(self.sector.maps[i])):
                if self.sector.maps[i][j] == '0':
                    self.sector_view[i].append(render.LIGHT_GROUND)
                elif self.sector.maps[i][j] == '1':
                    self.sector_view[i].append(random.choice(
                        [render.LIGHT_WALL, render.LIGHT_WALL1]))
                elif self.sector.maps[i][j] == '2':
                    self.sector_view[i].append(render.PLAYER)
                elif self.sector.maps[i][j] == '3':
                    self.sector_view[i].append(render.MOB)
                elif self.sector.maps[i][j] == '4':
                    self.sector_view[i].append(render.LADDER)
                elif self.sector.maps[i][j] == '5':
                    self.sector_view[i].append(render.CHEST)
            self.sector_view.append([])

    @property
    def get_fps(self):
        return self.FPS

    @property
    def getWindow(self):
        return self.__WINDOW_HEIGHT, self.__WINDOW_WEIGHT

    def get_view(self):
        startI = self.player.location[0] - 2
        endI = startI + 5
        startJ = self.player.location[1] - 2
        endJ = startJ + 5
        view = [['1'] * 5 for i in range(5)]
        x = 0
        y = 0
        for i in range(startI, endI):
            for j in range(startJ, endJ):
                view[x][y] = self.sector.maps[i][j]
                y += 1
            x += 1
            y = 0
        return view

    def renderView(self):
        render.renderGame(self.sc, self.sector.maps, self.player, self.level, len(self.sector.mobs),
                          self.sector_view)

    def initPlayer(self):
        self.player.hp = 10
        self.player.armor = 0
        self.player.armor_lvl = 0
        self.player.weapon_lvl = 0
        self.player.power = 1
        self.player.inventory = ['', '', '', '', '', '']
        self.player.location = self.sector.setPlayer()
        self.player.view_location = [32 * 5, 32 * 5]

    def restartLevel(self, new_player):
        self.sc.fill((0, 0, 0))
        self.sector.__init__(level=self.level)
        self.sector_view_append()
        if new_player:
            self.initPlayer()
        else:
            self.player.location = self.sector.setPlayer()

    def increaseLevel(self):
        self.zero_mobs = False
        self.level += 1

    def movePlayer(self, dx, dy):
        self.player.location = self.sector.movePlayer(dx, dy, self.player)
        if self.player.location == [0, 0]:
            self.increaseLevel()
            self.restartLevel(False)
        else:
            return

    def moveMobs(self):
        self.sector.moveMobs(self.player, self.sc)

    def __searchMob(self, di, dj):
        tmp = self.sector.mobs
        for i in range(0, len(tmp)):
            if tmp[i].location == [self.player.location[0] + di, self.player.location[1] + dj]:
                tmp[i].hp = tmp[i].hp - self.player.power
                render.attackMob(
                    self.sc, [self.player.view_location[1] + di * 32, self.player.view_location[0] + dj * 32], False)
                if tmp[i].hp <= 0:
                    self.killed_mobs += 1
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
        pos = 0
        while mode:
            flag = False
            pygame.display.update()
            self.clock.tick(self.FPS)
            render.renderInfoAboutPlayer(
                self.sc, self.player, self.level, len(self.sector.mobs))
            render.renderInv(self.sc, self.player, mode, pos)

            if self.control_mode == 0:
                for e in pygame.event.get():
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_LEFT:
                            if pos != 0:
                                pos -= 1
                        elif e.key == pygame.K_RIGHT:
                            if pos != 5:
                                pos += 1
                        elif e.key == pygame.K_UP:
                            if pos not in [0, 1, 2]:
                                pos -= 3
                        elif e.key == pygame.K_DOWN:
                            if pos not in [3, 4, 5]:
                                pos += 3

                        elif e.key == pygame.K_e:
                            mode = False
                        elif e.key == pygame.K_q:
                            self.player.inventory[pos] = ''
                        elif e.key == pygame.K_SPACE:
                            flag = True
            else:
                mouse_pos = pygame.mouse.get_pos()
                # print(mouse_pos)
                if mouse_pos[0] >= 800 and mouse_pos[0] <= 853 and mouse_pos[1] >= 226 and mouse_pos[1] <= 279:
                    pos = 0
                elif mouse_pos[0] >= 854 and mouse_pos[0] <= 908 and mouse_pos[1] >= 226 and mouse_pos[1] <= 279:
                    pos = 1
                elif mouse_pos[0] >= 909 and mouse_pos[0] <= 959 and mouse_pos[1] >= 226 and mouse_pos[1] <= 279:
                    pos = 2
                elif mouse_pos[0] >= 800 and mouse_pos[0] <= 853 and mouse_pos[1] >= 278 and mouse_pos[1] <= 328:
                    pos = 3
                elif mouse_pos[0] >= 854 and mouse_pos[0] <= 908 and mouse_pos[1] >= 278 and mouse_pos[1] <= 328:
                    pos = 4
                elif mouse_pos[0] >= 909 and mouse_pos[0] <= 959 and mouse_pos[1] >= 278 and mouse_pos[1] <= 328:
                    pos = 5
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        quit()
                    elif e.type == pygame.MOUSEBUTTONDOWN:
                        if e.button == 1:
                            flag = True
                        if e.button == 3:
                            self.player.inventory[pos] = ''
                    elif e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_e:
                            mode = False

            if flag:
                selected_item = self.player.inventory[pos]
                if selected_item == '':
                    continue
                elif selected_item == 'potion':
                    if self.player.hp == 10:
                        continue
                    else:
                        self.player.hp += 1
                        self.player.inventory[pos] = ''
                elif selected_item[:len(selected_item) - 1] == 'disk_lvl':
                    if int(selected_item[len(selected_item) - 1]) <= self.player.weapon_lvl:
                        continue
                    else:
                        self.player.weapon_lvl = int(
                            selected_item[len(selected_item) - 1])
                        self.player.power = 1 + self.player.weapon_lvl
                        self.player.inventory[pos] = ''
                elif selected_item[:len(selected_item) - 1] == 'armor_lvl':
                    if int(selected_item[len(selected_item) - 1]) <= self.player.armor_lvl:
                        continue
                    else:
                        self.player.armor_lvl = int(
                            selected_item[len(selected_item) - 1])
                        self.player.inventory[pos] = ''

    def enter_name(self, ):
        size = 16
        name = []
        curr_index = 0

        while True:
            pygame.display.update()
            self.clock.tick(self.FPS)

            if len(name) >= 24:
                continue

            f = pygame.font.Font('src/Minecraftia.ttf', size)

            t = f.render('Enter your name', 0, (255, 255, 255))
            self.sc.blit(t, (0, 0))
            x = 0
            for i in name:
                t = f.render(i, 0, (255, 255, 255))
                x += size
                self.sc.blit(t, (x, size * 3))
            pass

            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        curr_index -= 1
                        del name[curr_index]
                        self.sc.fill((0, 0, 0))
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
                        name += 't'
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
                        name += '/'
                    elif e.key == pygame.K_EXCLAIM:
                        name += '!'
                    elif e.key == pygame.K_QUOTEDBL:
                        name += '"'
                    elif e.key == pygame.K_HASH:
                        name += '#'
                    elif e.key == pygame.K_DOLLAR:
                        name += '$'
                    elif e.key == pygame.K_AMPERSAND:
                        name += '&'
                    elif e.key == pygame.K_LEFTPAREN:
                        name += '('
                    elif e.key == pygame.K_RIGHTPAREN:
                        name += ')'
                    elif e.key == pygame.K_RETURN:
                        sql = "select username from users where username='" + \
                              ''.join(name) + "'"
                        if cursor.execute(sql):
                            tmp_username = cursor.fetchone()
                            if tmp_username != None:
                                self.username = ''.join(name)
                            else:
                                sql = 'insert into users (username, highest_level, max_mobs) values ("' + ''.join(
                                    name) + '", 0, 0)'
                                cursor.execute(sql)
                                conn.commit()
                                self.username = ''.join(name)
                        self.sc.fill((0, 0, 0))
                        return
                    # self.sc.fill((0,0,0))
                    curr_index += 1

    def renderMenu(self, pos, InProccess):
        # sc.fill((0, 0, 0))
        f = pygame.font.Font('src/Minecraftia.ttf', 48)
        if InProccess:
            menu = ['return', 'restart', 'settings', 'exit']
            y = 180
        else:
            menu = ['start', 'stats', 'settings', 'exit']
            y = 180
        for i in range(0, len(menu)):
            if i == pos:
                t = f.render(menu[i], 0, (255, 255, 0))
            else:
                t = f.render(menu[i], 0, (255, 255, 255))
            self.sc.blit(t, (0, y))
            y += 72
        return menu

    def show_stats(self):
        self.sc.fill((0, 0, 0))
        size = 30
        while True:

            pygame.display.update()
            self.clock.tick(self.FPS)

            sql = 'select * from users'
            result = cursor.execute(sql)

            f = pygame.font.Font('src/Minecraftia.ttf', size)
            t = f.render('username      highest_level      Mob_kills', 0, (255, 255, 255))
            self.sc.blit(t, (0, 0))
            t = f.render('==========================================', 0, (255, 255, 255))
            self.sc.blit(t, (0, size))
            c = 2
            for row in result:
                t = f.render(str(row[0]), 0, (255, 255, 255))
                self.sc.blit(t, (0, size * c))
                t = f.render(str(row[1]), 0, (255, 255, 255))
                self.sc.blit(t, (size * 10, size * c))
                t = f.render(str(row[2]), 0, (255, 255, 255))
                self.sc.blit(t, (size * 22, size * c))
                c += 1
            c += 1
            t = f.render('BACK', 0, (255, 255, 0))
            self.sc.blit(t, (0, size * c))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                if self.control_mode == 0:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_RETURN:
                            return
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    if e.type == pygame.MOUSEBUTTONDOWN and 0 <= mouse_pos[0] <= 138 and mouse_pos[
                        1] >= size*c and mouse_pos[1] <= size*(c+2):
                        return

    def show_settings(self):
        f = pygame.font.Font('src/Minecraftia.ttf', 48)
        self.sc.fill((0, 0, 0))
        curr_pos = 0
        while True:
            pygame.display.update()
            self.clock.tick(self.FPS)

            t = f.render('CONTROL SETTINGS', 0, (255, 255, 255))
            self.sc.blit(t, (0, 0))
            curr_mode = 'KEYBOARD + MOUSE' if self.control_mode else 'ONLY KEYBOARD'
            curr_menu = [['MODE:', curr_mode], 'BACK']

            for i in curr_menu:
                if isinstance(i, list):
                    if curr_pos == 0:
                        t = f.render(i[0], 0, (255, 255, 0))
                    else:
                        t = f.render(i[0], 0, (255, 255, 255))
                    self.sc.blit(t, (0, 48))
                    t = f.render(i[1], 0, (255, 255, 255))
                    self.sc.blit(t, (300, 48))
                else:
                    if curr_pos == 1:
                        t = f.render(i, 0, (255, 255, 0))
                    else:
                        t = f.render(i, 0, (255, 255, 255))
                    self.sc.blit(t, (0, 48 * 3))

            if self.control_mode:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                    pressed = pygame.mouse.get_pressed()
                    pos = pygame.mouse.get_pos()
                    if pos[0] <= 150 and pos[0] >= 0 and pos[1] >= 66 and pos[1] <= 107:
                        curr_pos = 0
                    elif pos[0] >= 0 and pos[0] <= 137 and pos[1] >= 163 and pos[1] <= 204:
                        curr_pos = 1

                    if pressed[0]:
                        # print(pos)
                        if pos[0] <= 150 and pos[0] >= 0 and pos[1] >= 66 and pos[1] <= 107:
                            self.control_mode = 0
                            self.sc.fill((0, 0, 0))
                        elif pos[0] >= 0 and pos[0] <= 137 and pos[1] >= 163 and pos[1] <= 204:
                            self.sc.fill((0, 0, 0))
                            return
            else:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        quit()
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_RETURN:
                            if curr_pos == 1:
                                self.sc.fill((0, 0, 0))
                                return
                            else:
                                self.sc.fill((0, 0, 0))
                                self.control_mode = 1
                        elif e.key == pygame.K_UP:
                            if curr_pos != 0:
                                curr_pos = 0
                        elif e.key == pygame.K_DOWN:
                            if curr_pos != 1:
                                curr_pos = 1

    def menu(self, InProccess, firstStart):

        if firstStart:
            self.enter_name()

        menu = True
        pos = 0
        while menu:
            pygame.display.update()
            self.clock.tick(self.FPS)

            list_menu = self.renderMenu(pos, InProccess)
            length_menu = len(list_menu)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                if self.control_mode == 0:
                    if e.type == pygame.KEYDOWN:
                        if e.key == pygame.K_DOWN:
                            if pos + 1 > length_menu - 1:
                                pass
                            else:
                                pos += 1
                        elif e.key == pygame.K_UP:
                            if pos - 1 < 0:
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
                                self.sc.fill((0, 0, 0))
                            elif list_menu[pos] == 'settings':
                                self.show_settings()
                            elif list_menu[pos] == 'exit':
                                quit()
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    # print(mouse_pos)

                    if mouse_pos[0] >= 0 and mouse_pos[0] <= 153 and mouse_pos[1] >= 198 and mouse_pos[1] <= 242:
                        pos = 0
                        if e.type == pygame.MOUSEBUTTONDOWN:
                            if e.button == 1:
                                if list_menu[pos] == 'start' or list_menu[pos] == 'return':
                                    menu = False

                    elif mouse_pos[0] >= 0 and mouse_pos[0] <= 151 and mouse_pos[1] >= 271 and mouse_pos[1] <= 314:
                        pos = 1
                        if e.type == pygame.MOUSEBUTTONDOWN:
                            if e.button == 1:
                                if list_menu[pos] == 'stats':
                                    self.show_stats()
                                    self.sc.fill((0, 0, 0))
                                else:
                                    self.restartLevel(True)
                                    menu = False

                    elif mouse_pos[0] >= 0 and mouse_pos[0] <= 234 and mouse_pos[1] >= 342 and mouse_pos[1] <= 391:
                        pos = 2
                        if e.type == pygame.MOUSEBUTTONDOWN:
                            if e.button == 1:
                                if list_menu[pos] == 'settings':
                                    self.show_settings()

                    elif mouse_pos[0] >= 0 and mouse_pos[0] <= 104 and mouse_pos[1] >= 419 and mouse_pos[1] <= 459:
                        pos = 3
                        if e.type == pygame.MOUSEBUTTONDOWN:
                            if e.button == 1:
                                if list_menu[pos] == 'exit':
                                    quit()

    def checkChest(self):
        x = self.player.location[0]
        y = self.player.location[1]
        if self.sector.maps[x - 1][y] == '5':
            return [x - 1, y]
        elif self.sector.maps[x + 1][y] == '5':
            return [x + 1, y]
        elif self.sector.maps[x][y - 1] == '5':
            return [x, y - 1]
        elif self.sector.maps[x][y + 1] == '5':
            return [x, y + 1]
        else:
            return []

    def addToInvFromChest(self, item):
        pos = 0
        for i in self.player.inventory:
            if i == '':
                self.player.inventory[pos] = item
                return
            else:
                pos += 1

    def openChest(self):
        loc = self.checkChest()
        if loc != []:
            r = random.randint(1, 3)
            if r in [1, 2]:
                self.addToInvFromChest('potion')
                self.sector.maps[loc[0]][loc[1]] = '0'
                return
            else:
                r = random.randint(1, 2)

                if r == 1:
                    item = 'disk_lvl' + str(self.player.weapon_lvl + 1)
                    self.addToInvFromChest(item)
                    self.sector.maps[loc[0]][loc[1]] = '0'
                    return
                else:

                    item = 'armor_lvl' + str(self.player.weapon_lvl + 1)
                    self.addToInvFromChest(item)
                    self.sector.maps[loc[0]][loc[1]] = '0'
                    return
        else:
            return

    def check_mouse_pos(self, pos):
        # print(pos)
        # print(self.player.view_location)
        pl = self.player.view_location
        up_sprite = ((self.player.view_location[0], self.player.view_location[1] - 32),
                     (self.player.view_location[0] + 32, self.player.view_location[1] - 1))
        right_sprite = ((self.player.view_location[0] + 32, self.player.view_location[1]),
                        (self.player.view_location[0] + 32 + 32, self.player.view_location[1] + 32))
        down_sprite = ((self.player.view_location[0], self.player.view_location[1] + 32),
                       (self.player.view_location[0] + 32, self.player.view_location[1] + 32 * 2))
        left_sprite = ((self.player.view_location[0] - 32, self.player.view_location[1]),
                       (self.player.view_location[0] - 1, self.player.view_location[1] + 32))

        if pos[0] >= up_sprite[0][0] and pos[0] <= up_sprite[1][0] and pos[1] >= up_sprite[0][1] and pos[1] <= \
                up_sprite[1][1]:
            obj = self.sector.maps[self.player.location[0] -
                                   1][self.player.location[1]]
        elif pos[0] >= right_sprite[0][0] and pos[0] <= right_sprite[1][0] and pos[1] >= right_sprite[0][1] and pos[
            1] <= right_sprite[1][1]:
            obj = self.sector.maps[self.player.location[0]
            ][self.player.location[1] + 1]
        elif pos[0] >= down_sprite[0][0] and pos[0] <= down_sprite[1][0] and pos[1] >= down_sprite[0][1] and pos[1] <= \
                down_sprite[1][1]:
            obj = self.sector.maps[self.player.location[0] +
                                   1][self.player.location[1]]
        elif pos[0] >= left_sprite[0][0] and pos[0] <= left_sprite[1][0] and pos[1] >= left_sprite[0][1] and pos[1] <= \
                left_sprite[1][1]:
            obj = self.sector.maps[self.player.location[0]
            ][self.player.location[1] - 1]
        else:
            return
        if obj == '3':
            self.playerAttackMob()
        elif obj == '5':
            self.openChest()
        # print(up_sprite,right_sprite,down_sprite,left_sprite)
        return

    def post_event(self, tpe):
        #
        ev = pygame.event.Event(pygame.KEYDOWN, {'key': tpe})
        pygame.event.post(ev)

    def cycle(self):
        # while True:
        self.clock.tick(self.FPS)
        pygame.display.update()
        self.renderView()
        # move_key = False
        if self.player.hp <= 0:
            if self.god_mode == 1:
                pass
            else:
                sql = 'select highest_level from users where username="' + \
                      str(self.username) + '"'
                cursor.execute(sql)
                result = cursor.fetchone()
                if int(result[0]) < self.level:
                    sql = 'update users set highest_level=' + \
                          str(self.level) + ' where username="' + \
                          str(self.username) + '"'
                    cursor.execute(sql)
                    conn.commit()

                sql = 'select max_mobs from users where username="' + \
                      str(self.username) + '"'
                cursor.execute(sql)
                result = cursor.fetchone()
                if int(result[0]) < self.killed_mobs:
                    sql = 'update users set max_mobs=' + \
                          str(self.killed_mobs) + ' where username="' + \
                          str(self.username) + '"'
                    cursor.execute(sql)
                    conn.commit()
                    self.killed_mobs = 0

                self.sc.fill((255, 0, 0))
                f = pygame.font.Font('src/Minecraftia.ttf', 48)
                gameover_text = f.render("GAME OVER", 0, (0, 0, 0))
                self.sc.blit(gameover_text, (250, 250))
                pygame.display.update()
                time.sleep(2)
                self.level = 1
                self.restartLevel(True)
                self.menu(False, False)

        if self.control_mode == 0:
            keys = pygame.key.get_pressed()
            delay = 2
            if keys[pygame.K_UP]:
                if self.move_clk == delay:
                    self.movePlayer(-1, 0)
                    self.move_clk = 0
                else:
                    self.move_clk += 1
            elif keys[pygame.K_DOWN]:
                if self.move_clk == delay:
                    self.movePlayer(1, 0)
                    self.move_clk = 0
                else:
                    self.move_clk += 1
            elif keys[pygame.K_RIGHT]:
                if self.move_clk == delay:
                    self.movePlayer(0, 1)
                    self.move_clk = 0
                else:
                    self.move_clk += 1
            elif keys[pygame.K_LEFT]:
                if self.move_clk == delay:
                    self.movePlayer(0, -1)
                    self.move_clk = 0
                else:
                    self.move_clk += 1

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    exit()
                elif i.type == pygame.KEYDOWN:
                    # game.printLog()
                    if i.key == pygame.K_SPACE:
                        self.playerAttackMob()
                        move_key = True
                    elif i.key == pygame.K_p:
                        if not self.god_mode:
                            self.god_mode = True
                        else:
                            self.god_mode = False
                    elif i.key == pygame.K_r:
                        self.openChest()
                    elif i.key == pygame.K_ESCAPE:
                        self.menu(True, False)
                    elif i.key == pygame.K_e:
                        self.inv_mode()
        else:
            keys = pygame.key.get_pressed()
            delay = 2
            if keys[pygame.K_w]:
                if self.move_clk == delay:
                    self.movePlayer(-1, 0)
                    self.move_clk = 0
                else:
                    self.move_clk += 1
            elif keys[pygame.K_s]:
                if self.move_clk == delay:
                    self.movePlayer(1, 0)
                    self.move_clk = 0
                else:
                    self.move_clk += 1
            elif keys[pygame.K_d]:
                if self.move_clk == delay:
                    self.movePlayer(0, 1)
                    self.move_clk = 0
                else:
                    self.move_clk += 1
            elif keys[pygame.K_a]:
                if self.move_clk == delay:
                    self.movePlayer(0, -1)
                    self.move_clk = 0
                else:
                    self.move_clk += 1
            for i in pygame.event.get():

                if i.type == pygame.KEYDOWN:
                    if i.key == pygame.K_p:
                        if not self.god_mode:
                            self.god_mode = True
                        else:
                            self.god_mode = False
                    elif i.key == pygame.K_r:
                        self.openChest()
                    elif i.key == pygame.K_ESCAPE:
                        self.menu(True, False)
                    elif i.key == pygame.K_SPACE:
                        self.playerAttackMob()
                    elif i.key == pygame.K_e:
                        self.inv_mode()
                elif i.type == pygame.MOUSEBUTTONDOWN:
                    # game.printLog()
                    if i.button == 1:
                        self.check_mouse_pos(pygame.mouse.get_pos())

            # for i in pygame.event.get():
            #     if i.type == pygame.QUIT:
            #         exit()

            #             # game.playerAttackMob()
            #             # move_key = True
            #     elif i.type == pygame.KEYDOWN:
            #         if i.key == pygame.K_p:
            #             if not self.god_mode:
            #                 self.god_mode = True
            #             else:
            #                 self.god_mode = False
            #         # elif i.key == pygame.K_r:
            #         #     game.openChest()
            #         elif i.key == pygame.K_ESCAPE:
            #             self.menu(True, False)
            #         elif i.key == pygame.K_e:
            #             self.inv_mode()

        if self.mob_clk == int(self.FPS / 3):
            self.moveMobs()
            self.mob_clk = 0
        else:
            self.mob_clk += 1

        if len(self.sector.mobs) == 0 and not self.zero_mobs:
            self.addToInvFromChest('potion')
            zero_mobs = True


game = Game(1)
while True:
    game.cycle()
