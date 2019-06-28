import random
import math
import entities
import render


class Room():
    x1=0
    x2=0

    y1=0
    y2=0

    def __init__(self,x1,x2,y1,y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

class Map(object):
    length = 25
    maps = []
    center = []
    rooms = []
    chests = []
    mobs = []
    def __init__(self):
        self.maps = [['1' for i in range(0, self.length)] for j in range(0, self.length)]
        countofrooms = random.randint(3,5)
        self.generateroom(countofrooms, True)
        countofchests = random.randint(1, 2)
        self.setChests(countofchests, 1)
        self.setLadder()
        countofmobs = random.randint(len(self.center) // 2, len(self.center))
        self.setMobs(countofmobs, 1)

    def cleanUp(self):
        self.maps = [['1' for i in range(0, self.length)] for j in range(0, self.length)]
        self.center = []
        self.chests = []
        self.mobs = []
        self.rooms = []

    def generatetunnels(self, n):
        firstcenter = self.center[n - 1]
        secondcenter = self.center[n]

        for i in range(min(firstcenter[0], secondcenter[0]), max(firstcenter[0], secondcenter[0]) + 1):
            self.maps[i][secondcenter[1]] = '0'
        for j in range(min(firstcenter[1], secondcenter[1]), max(firstcenter[1], secondcenter[1]) + 1):
            self.maps[firstcenter[0]][j] = '0'

    def check_intersection(self,r, newroom):
        if (r.x1 <= newroom.x2 and r.x2>=newroom.x1 and r.y1 <= newroom.y2 and r.y2>= newroom.y1):
            return True
        else:
            return False

    def generateroom(self, countofrooms, tunnels):
        n=0
        c=0
        while n < countofrooms:
            w = random.randint(4, 6)
            h = random.randint(4, 6)
            x1 = random.randint(1, self.length - w - 1)
            x2 = x1 + w
            y1 = random.randint(1, self.length - h - 1)
            y2 = y1 + h
            newroom = Room(x1,x2,y1,y2)
            failed = False
            for r in self.rooms:
                if self.check_intersection(r,newroom):
                    failed = True
                    break
            if failed:
                continue
            self.rooms.append(newroom)
            self.center.append([math.floor((x1 + x2) / 2), math.floor((y1 + y2) / 2)])
            for i in range(x1, x2):
                for j in range(y1, y2):
                    self.maps[i][j] = '0'
            if tunnels:
                if n != 0:
                    self.generatetunnels(n)
            n+=1
            if c>100:
                c=0
                n=0
                self.rooms=[]
                self.center=[]
                self.maps = [['1' for i in range(0, self.length)] for j in range(0, self.length)]

            

        print("System generated " + str(countofrooms) + " rooms")

    def setChests(self, count, level):
        i = 0
        while i < count:
            locate = random.choice(self.center)
            x = locate[0] + random.randint(-2, 2)
            y = locate[1] + random.randint(-2, 2)
            if self.maps[x][y] == '0':
                flag = False
                for i in range(x-2,x+2):
                    for j in range(y-2,y+2):
                        if self.maps[i][j] == '5':
                            flag = True
                if flag:
                    continue
                else:
                    self.chests.append(entities.Chest(i, level, x, y))
                    self.maps[x][y] = '5'
                    i += 1
            else:
                continue
        print(self.chests)

    def setLadder(self):
        while True:
            i = random.randint(0,len(self.center)-1)
            curr = self.center[i]
            x = curr[0]
            y = curr[1]
            if self.maps[x][y] == '0':
                self.maps[x][y] = '4'
                return

    def setMobs(self, count, level):
        i = 0
        while i < count:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.length - 1)

            flag = False
            for k in range(x-1,x+1):
                for l in range(y-1,y+1):
                    if self.maps[k][l]=='2':
                        flag=True
            if flag:
                continue

            if self.maps[x][y] == '0':
                self.mobs.append(entities.Mob(i, level, x, y))
                self.maps[x][y] = '3'
                i += 1

    def moveCurrentMob(self, mob, player, sc):
        cur_i = mob.location[0]
        cur_j = mob.location[1]
        find_player = False
        for i in range(cur_i - 3, cur_i + 3):
            for j in range(cur_j - 3, cur_j + 3):
                if i>=len(self.maps) or i<0 or j>=len(self.maps) or j<0:
                    continue
                if self.maps[i][j] == '2':
                    find_player = True
        if not find_player:
            if self.maps[cur_i - 1][cur_j] == '0' or self.maps[cur_i + 1][cur_j] == '0' or self.maps[cur_i][
                cur_j - 1] == '0' or self.maps[cur_i][cur_j + 1] == '0':
                while True:
                    di = random.randint(-1, 1)
                    dj = random.randint(-1, 1)
                    if di != 0 and dj != 0:
                        continue
                    else:
                        if self.maps[cur_i + di][cur_j + dj] in ['1', '2', '3', '4', '5']:
                            continue
                        else:
                            break
                self.maps[cur_i][cur_j] = '0'
                mob.location[0] += di
                mob.location[1] += dj
                self.maps[cur_i + di][cur_j + dj] = '3'
        else:
            if self.maps[cur_i + 1][cur_j] == '2' or self.maps[cur_i][cur_j + 1] == '2' or self.maps[cur_i - 1][
                cur_j] == '2' or self.maps[cur_i][cur_j - 1] == '2':
                player.hp -= mob.power - player.armor_lvl
                render.attackMob(sc, player.location)
            else:
                diffI = player.location[0] - cur_i
                diffJ = player.location[1] - cur_j
                di = []
                dj = []
                if diffI < 0 and diffJ < 0:  # в зависимости от разницы составляются "векторы" направления моба
                    di = [-2, -1]
                    dj = [-2, -1]
                elif diffI > 0 and diffJ < 0:
                    di = [2, 1]
                    dj = [-2, -1]
                elif diffI < 0 and diffJ > 0:
                    di = [-2, -1]
                    dj = [2, 1]
                elif diffI > 0 and diffJ > 0:
                    di = [2, 1]
                    dj = [2, 1]
                elif diffI == 0 and diffJ <= 0:
                    di = [0, 0]
                    dj = [-2, -1]
                elif diffI == 0 and diffJ >= 0:
                    di = [0, 0]
                    dj = [2, 1]
                elif diffI <= 0 and diffJ == 0:
                    di = [-2, -1]
                    dj = [0, 0]
                elif diffI >= 0 and diffJ == 0:
                    di = [2, 1]
                    dj = [0, 0]
                else:
                    pass

                flag = False
                newI = 0
                newJ = 0
                for i in di:
                    for j in dj:
                        if self.maps[cur_i + i][cur_j + j] == '0':
                            flag = True
                            newI = i
                            newJ = j
                            break
                    if flag:
                        break
                if flag:
                    mob.location[0] = cur_i + newI
                    mob.location[1] = cur_j + newJ
                    self.maps[cur_i][cur_j] = '0'
                    self.maps[cur_i + newI][cur_j + newJ] = '3'

    def moveMobs(self, player, sc):
        for mob in self.mobs:
            self.moveCurrentMob(mob, player, sc)

    def setPlayer(self):
        while True:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.length - 1)
            if self.maps[x][y] == '0':
                self.maps[x][y] = '2'
                return [x, y]

    def movePlayer(self, dx, dy, player):
        future_place = self.maps[player.location[0] + dx][player.location[1] + dy]
        if future_place in ['1', '3', '5']:
            return player.location
        elif future_place == '4':
            return [0, 0]
        else:
            self.maps[player.location[0]][player.location[1]] = '0'
            player.location[0] += dx
            player.location[1] += dy
            self.maps[player.location[0]][player.location[1]] = '2'
            return player.location
