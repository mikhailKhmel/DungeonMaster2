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
    player = entities.Player(id=0, location=sector.setPlayer(), view_location=[32 * 10, 32 * 10])
    username = ''
    control_mode = 1  # 0 - only keyboard. 1 - keyboard and mouse

    def __init__(self, level):
        self.level = level
        self.__FPS = 20
        self.__STEP = 16
        self.__WINDOW_HEIGHT = 960
        self.__WINDOW_WEIGHT = 800
        self.sector_view_append()

    def sector_view_append(self):
        self.sector_view = [[]]
        for i in range(0, len(self.sector.maps)):
            for j in range(0, len(self.sector.maps[i])):
                if self.sector.maps[i][j] == '0':
                    self.sector_view[i].append(render.LIGHT_GROUND)
                elif self.sector.maps[i][j] == '1':
                    self.sector_view[i].append(random.choice([render.LIGHT_WALL, render.LIGHT_WALL1]))
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
    def getFps(self):
        return self.__FPS

    @property
    def getStep(self):
        return self.__STEP

    @property
    def getWindow(self):
        return self.__WINDOW_HEIGHT, self.__WINDOW_WEIGHT

    def renderView(self, god_mode, seconds):
        render.renderGame(sc, self.sector.maps, god_mode, self.player, self.level, len(self.sector.mobs),
                          self.sector_view, seconds)

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
        sc.fill((0, 0, 0))
        self.sector.__init__(level=self.level)
        self.sector_view_append()
        if new_player:
            self.initPlayer()
        else:
            self.player.location = self.sector.setPlayer()

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
        if self.sector.maps[self.player.location[0] + di][self.player.location[1] + dj] == '3':
            tmp = self.sector.mobs
            for i in range(0, len(tmp)):
                if tmp[i].location == [self.player.location[0] + di, self.player.location[1] + dj]:
                    tmp[i].hp = tmp[i].hp - self.player.power
                    render.attackMob(sc,
                                     [self.player.view_location[1] + di * 32, self.player.view_location[0] + dj * 32],
                                     False)
                    if tmp[i].hp <= 0:
                        tmp.remove(tmp[i])
                        self.sector.maps[self.player.location[0] +
                                         di][self.player.location[1] + dj] = '0'
                    self.sector.mobs = tmp
                    return
        elif self.sector.maps[self.player.location[0] + di][self.player.location[1] + dj] == '6':
            tmp = self.sector.boss
            for i in range(0, len(tmp)):
                if tmp[i].location == [self.player.location[0] + di, self.player.location[1] + dj]:
                    tmp[i].hp = tmp[i].hp - self.player.power
                    render.attackMob(sc,
                                     [self.player.view_location[1] + di * 32, self.player.view_location[0] + dj * 32],
                                     False)
                    if tmp[i].hp <= 0:
                        tmp.remove(tmp[i])
                        self.sector.maps[self.player.location[0] +
                                         di][self.player.location[1] + dj] = '0'
                        for item in ['potion', 'glasses']:
                            self.addToInvFromChest(item)
                    self.sector.boss = tmp
                    return


    def playerAttackMob(self):
        current_locationI = self.player.location[0]
        current_locationJ = self.player.location[1]
        if self.sector.maps[current_locationI + 1][current_locationJ] == '3' or self.sector.maps[current_locationI + 1][
            current_locationJ] == '6':
            self.__searchMob(1, 0)
        elif self.sector.maps[current_locationI][current_locationJ + 1] == '3' or self.sector.maps[current_locationI][
            current_locationJ + 1] == '6':
            self.__searchMob(0, 1)
        elif self.sector.maps[current_locationI - 1][current_locationJ] == '3' or \
                self.sector.maps[current_locationI - 1][current_locationJ] == '6':
            self.__searchMob(-1, 0)
        elif self.sector.maps[current_locationI][current_locationJ - 1] == '3' or self.sector.maps[current_locationI][
            current_locationJ - 1] == '6':
            self.__searchMob(0, -1)

    def inv_mode(self):
        mode = True
        pos = 0
        while mode:
            flag = False
            pygame.display.update()
            clock.tick(self.getFps)
            render.renderInfoAboutPlayer(sc, self.player, self.level, len(self.sector.mobs), 11)
            render.renderInv(sc, self.player, mode, pos, True)

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
                        self.player.weapon_lvl = int(selected_item[len(selected_item) - 1])
                        self.player.power = 1 + self.player.weapon_lvl
                        self.player.inventory[pos] = ''
                elif selected_item[:len(selected_item) - 1] == 'armor_lvl':
                    if int(selected_item[len(selected_item) - 1]) <= self.player.armor_lvl:
                        continue
                    else:
                        self.player.armor_lvl = int(selected_item[len(selected_item) - 1])
                        self.player.inventory[pos] = ''
                elif selected_item == 'glasses':
                    self.player.inventory[pos] = ''
                    self.using_glasses()

    def using_glasses(self):
        global god_mode
        god_mode = True

    def enter_name(self, sc):
        size = 16
        name = []
        curr_index = 0

        while True:
            pygame.display.update()
            clock.tick(self.getFps)

            if len(name) >= 24:
                continue

            f = pygame.font.Font('src/Minecraftia.ttf', size)

            t = f.render('Enter your name', 0, (255, 255, 255))
            sc.blit(t, (0, 0))
            x = 0
            for i in name:
                t = f.render(i, 0, (255, 255, 255))
                x += size
                sc.blit(t, (x, size * 3))
            pass

            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        curr_index -= 1
                        del name[curr_index]
                        sc.fill((0, 0, 0))
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
                        sql = "select username from users where username='" + ''.join(name) + "'"
                        if cursor.execute(sql):
                            tmp_username = cursor.fetchone()
                            if tmp_username != None:
                                self.username = ''.join(name)
                            else:
                                sql = 'insert into users (username, highest_level) values ("' + ''.join(name) + '", 0)'
                                cursor.execute(sql)
                                conn.commit()
                                self.username = ''.join(name)
                        sc.fill((0, 0, 0))
                        return
                    # sc.fill((0,0,0))
                    curr_index += 1

    def renderMenu(self, sc, pos, InProccess):
        # sc.fill((0, 0, 0))
        f = pygame.font.Font('src/Minecraftia.ttf', 48)
        if InProccess:
            menu = ['return', 'restart', 'exit']  # removed 'settings'
            y = 180
        else:
            menu = ['start', 'stats', 'exit']
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
        sc.fill((0, 0, 0))
        while True:

            pygame.display.update()
            clock.tick(self.getFps)

            sql = 'select * from users'
            result = cursor.execute(sql)

            f = pygame.font.Font('src/Minecraftia.ttf', 48)
            t = f.render('username      highest_level', 0, (255, 255, 255))
            sc.blit(t, (0, 0))
            t = f.render('==========================', 0, (255, 255, 255))
            sc.blit(t, (0, 48))
            c = 2
            for row in result:
                t = f.render(str(row[0]), 0, (255, 255, 255))
                sc.blit(t, (0, 48 * c))
                t = f.render(str(row[1]), 0, (255, 255, 255))
                sc.blit(t, (48 * 10, 48 * c))
                c += 1
            c += 1
            t = f.render('BACK', 0, (255, 255, 0))
            sc.blit(t, (0, 48 * c))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    quit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        return
                else:
                    mouse_pos = pygame.mouse.get_pos()
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if 0 <= mouse_pos[0] <= 138 and mouse_pos[1] >= 48 * c and mouse_pos[1] <= 48 * (c + 1):
                            return

    # def show_settings(self):
    #     f = pygame.font.Font('src/Minecraftia.ttf', 48)
    #     sc.fill((0, 0, 0))
    #     curr_pos = 0
    #     while True:
    #         pygame.display.update()
    #         clock.tick(self.getFps)
    #
    #         t = f.render('CONTROL SETTINGS', 0, (255, 255, 255))
    #         sc.blit(t, (0, 0))
    #         curr_mode = 'KEYBOARD + MOUSE' if self.control_mode else 'ONLY KEYBOARD'
    #         curr_menu = [['MODE:', curr_mode], 'BACK']
    #
    #         for i in curr_menu:
    #             if isinstance(i, list):
    #                 if curr_pos == 0:
    #                     t = f.render(i[0], 0, (255, 255, 0))
    #                 else:
    #                     t = f.render(i[0], 0, (255, 255, 255))
    #                 sc.blit(t, (0, 48))
    #                 t = f.render(i[1], 0, (255, 255, 255))
    #                 sc.blit(t, (300, 48))
    #             else:
    #                 if curr_pos == 1:
    #                     t = f.render(i, 0, (255, 255, 0))
    #                 else:
    #                     t = f.render(i, 0, (255, 255, 255))
    #                 sc.blit(t, (0, 48 * 3))
    #
    #         if self.control_mode:
    #             for event in pygame.event.get():
    #                 if event.type == pygame.QUIT:
    #                     quit()
    #                 pressed = pygame.mouse.get_pressed()
    #                 pos = pygame.mouse.get_pos()
    #                 if 150 >= pos[0] >= 0 and 66 <= pos[1] <= 107:
    #                     curr_pos = 0
    #                 elif 0 <= pos[0] <= 137 and 163 <= pos[1] <= 204:
    #                     curr_pos = 1
    #
    #                 if pressed[0]:
    #                     # print(pos)
    #                     if 0 <= pos[0] <= 150 <= pos[1] <= 107:
    #                         self.control_mode = 0
    #                         sc.fill((0, 0, 0))
    #                     elif 0 <= pos[0] <= 137 and 163 <= pos[1] <= 204:
    #                         sc.fill((0, 0, 0))
    #                         return
    #         else:
    #             for e in pygame.event.get():
    #                 if e.type == pygame.QUIT:
    #                     quit()
    #                 if e.type == pygame.KEYDOWN:
    #                     if e.key == pygame.K_RETURN:
    #                         if curr_pos == 1:
    #                             sc.fill((0, 0, 0))
    #                             return
    #                         else:
    #                             sc.fill((0, 0, 0))
    #                             self.control_mode = 1
    #                     elif e.key == pygame.K_UP:
    #                         if curr_pos != 0:
    #                             curr_pos = 0
    #                     elif e.key == pygame.K_DOWN:
    #                         if curr_pos != 1:
    #                             curr_pos = 1

    def menu(self, InProccess, sc, firstStart):

        if firstStart:
            self.enter_name(sc)

        menu = True
        pos = 0
        while menu:
            pygame.display.update()
            clock.tick(game.getFps)

            list_menu = game.renderMenu(sc, pos, InProccess)
            length_menu = len(list_menu)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()

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
                            sc.fill((0, 0, 0))
                        # elif list_menu[pos] == 'settings':
                        #     self.show_settings()
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
                                    sc.fill((0, 0, 0))
                                else:
                                    self.restartLevel(True)
                                    menu = False


                    # elif mouse_pos[0] >= 0 and mouse_pos[0] <= 234 and mouse_pos[1] >= 342 and mouse_pos[1] <= 391:
                    #     pos = 2
                    #     if e.type == pygame.MOUSEBUTTONDOWN:
                    #         if e.button == 1:
                    #             if list_menu[pos] == 'settings':
                    #                 self.show_settings()

                    elif mouse_pos[0] >= 0 and mouse_pos[0] <= 104 and mouse_pos[1] >= 342 and mouse_pos[1] <= 391:
                        pos = 2
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
            obj = self.sector.maps[self.player.location[0] - 1][self.player.location[1]]
        elif pos[0] >= right_sprite[0][0] and pos[0] <= right_sprite[1][0] and pos[1] >= right_sprite[0][1] and pos[
            1] <= right_sprite[1][1]:
            obj = self.sector.maps[self.player.location[0]][self.player.location[1] + 1]
        elif pos[0] >= down_sprite[0][0] and pos[0] <= down_sprite[1][0] and pos[1] >= down_sprite[0][1] and pos[1] <= \
                down_sprite[1][1]:
            obj = self.sector.maps[self.player.location[0] + 1][self.player.location[1]]
        elif pos[0] >= left_sprite[0][0] and pos[0] <= left_sprite[1][0] and pos[1] >= left_sprite[0][1] and pos[1] <= \
                left_sprite[1][1]:
            obj = self.sector.maps[self.player.location[0]][self.player.location[1] - 1]
        else:
            return
        if obj == '3':
            self.playerAttackMob()
        elif obj == '5':
            self.openChest()
        # print(up_sprite,right_sprite,down_sprite,left_sprite)
        return

    def printLog(self):
        print('LVL=', self.level)
        print('MAP')
        for i in self.sector.maps:
            print(i)
        print('MOBS')
        for i in self.sector.mobs:
            print('id=', i.id)
            print('location=', i.location)
            print('power=', i.power)
            print('hp=', i.hp)
            print('\n')
        print('ROOMS')
        for i in self.sector.rooms:
            print([i.x1, i.x2, i.y1, i.y2])
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
        print(self.sector.boss)

    def reference(self):
        flag = True
        while flag:
            render.renderInfoAboutControl(sc)
            pygame.display.update()
            clock.tick(self.getFps)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    exit()
                elif e.type == pygame.KEYDOWN:
                    if e.key in [pygame.K_ESCAPE, pygame.K_F1]:
                        flag = False


god_mode = False
zero_mobs = False
game = Game(1)

pygame.init()
sc = pygame.display.set_mode(game.getWindow)
lightZone = pygame.display.set_mode(game.getWindow)
sc.blit(lightZone, (0, 0))
clock = pygame.time.Clock()
###########

game.menu(False, sc, True)
game.renderView(god_mode, 0)

###########
pygame.display.update()
mob_clk = 0
move_clk = 0
god_mode_clk = 0
sec = 0
while True:
    fps = game.getFps
    clock.tick(fps)
    pygame.display.update()
    if god_mode:
        if god_mode_clk != fps * 10:
            god_mode_clk += 1
        else:
            god_mode_clk = 0
            god_mode = False
    game.renderView(god_mode, 11 - god_mode_clk // fps)
    move_key = False
    if game.player.hp <= 0:
        sql = 'select highest_level from users where username="' + str(game.username) + '"'
        cursor.execute(sql)
        result = cursor.fetchone()
        if int(result[0]) < game.level:
            sql = 'update users set highest_level=' + str(game.level) + ' where username="' + str(game.username) + '"'
            cursor.execute(sql)
            conn.commit()

        sc.fill((255, 0, 0))
        f = pygame.font.Font('src/Minecraftia.ttf', 48)
        gameover_text = f.render("GAME OVER", 0, (0, 0, 0))
        sc.blit(gameover_text, (250, 250))
        pygame.display.update()
        time.sleep(2)
        game.level = 1
        game.restartLevel(True)
        game.menu(False, sc, False)

    keys = pygame.key.get_pressed()
    delay = 2
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        if move_clk == delay:
            game.movePlayer(-1, 0)
            move_clk = 0
        else:
            move_clk += 1
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        if move_clk == delay:
            game.movePlayer(1, 0)
            move_clk = 0
        else:
            move_clk += 1
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        if move_clk == delay:
            game.movePlayer(0, 1)
            move_clk = 0
        else:
            move_clk += 1
    elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
        if move_clk == delay:
            game.movePlayer(0, -1)
            move_clk = 0
        else:
            move_clk += 1

    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
        elif i.type == pygame.KEYDOWN:
            # game.printLog()
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
            elif i.key == pygame.K_ESCAPE:
                game.menu(True, sc, False)
            elif i.key == pygame.K_e:
                game.inv_mode()
            elif i.key == pygame.K_F1:
                game.reference()


        elif i.type == pygame.MOUSEBUTTONDOWN:
            # game.printLog()
            if i.button == 1:
                game.check_mouse_pos(pygame.mouse.get_pos())
                # game.playerAttackMob()
                # move_key = True
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_p:
                if not god_mode:
                    god_mode = True
                else:
                    god_mode = False
            # elif i.key == pygame.K_r:
            #     game.openChest()
            elif i.key == pygame.K_ESCAPE:
                game.menu(True, sc, False)
            elif i.key == pygame.K_e:
                game.inv_mode()

    if mob_clk == int(fps / 3):
        game.moveMobs()
        mob_clk = 0
    else:
        mob_clk += 1

    if len(game.sector.mobs) == 0 and not zero_mobs:
        game.addToInvFromChest('potion')
        zero_mobs = True
