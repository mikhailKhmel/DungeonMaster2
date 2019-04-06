import random
import math
import entities


class Map(object):
    length = 64
    maps = []
    center = []
    chests = []
    mobs = []

    def __init__(self):
        self.maps = [['1' for i in range(0, self.length)] for j in range(0, self.length)]
        countofrooms = random.randint(5, 20)
        self.generateroom(countofrooms, True)
        countofchests = random.randint(len(self.center) // 2, len(self.center))
        self.setChests(countofchests, 1)
        self.setLadder()
        countofmobs = random.randint(len(self.center) // 2, len(self.center))
        self.setMobs(countofmobs, 1)

    def cleanUp(self):
        self.maps = []
        self.center = []
        self.chests = []
        self.mobs = []

    def generatetunnels(self, n):
        firstcenter = self.center[n - 1]
        secondcenter = self.center[n]

        for i in range(min(firstcenter[0], secondcenter[0]), max(firstcenter[0], secondcenter[0]) + 1):
            self.maps[i][secondcenter[1]] = '0'
        for j in range(min(firstcenter[1], secondcenter[1]), max(firstcenter[1], secondcenter[1]) + 1):
            self.maps[firstcenter[0]][j] = '0'

    def generateroom(self, countofrooms, tunnels):
        for n in range(0, countofrooms):
            w = random.randint(4, 10)
            h = random.randint(4, 10)
            x1 = random.randint(1, self.length - w - 1)
            x2 = x1 + w
            y1 = random.randint(1, self.length - h - 1)
            y2 = y1 + h
            self.center.append([math.floor((x1 + x2) / 2), math.floor((y1 + y2) / 2)])
            for i in range(x1, x2):
                for j in range(y1, y2):
                    self.maps[i][j] = '0'
            if tunnels:
                if n != 0:
                    self.generatetunnels(n)
        print("System generated " + str(countofrooms) + " rooms")

    def setChests(self, count, level):
        i = 0
        while i < count:
            locate = random.choice(self.center)
            x = locate[0] + random.randint(-2, 2)
            y = locate[1] + random.randint(-2, 2)
            if self.maps[x][y] == '0':
                self.chests.append(entities.Chest(i, level, x, y))
                self.maps[x][y] = '5'
                i += 1
        print(self.chests)

    def setLadder(self):
        while True:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.length - 1)
            if self.maps[x][y] == '0':
                self.maps[x][y] = '4'
                return

    def setMobs(self, count, level):
        i = 0
        while i < count:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.length - 1)
            if self.maps[x][y] == '0':
                self.mobs.append(entities.Mob(i, level, x, y))
                self.maps[x][y] = '3'
                i += 1

    def setPlayer(self):
        while True:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.length - 1)
            if self.maps[x][y] == '0':
                self.maps[x][y] = '2'
                entities.Player.location = [x, y]
                print(entities.Player.location)
                return [x, y]

    def movePlayer(self, dx, dy):
        future_place = self.maps[entities.Player.location[0] + dx][entities.Player.location[1] + dy]
        if future_place == '1':
            return False
        elif future_place == '4':
            return True
        else:
            self.maps[entities.Player.location[0]][entities.Player.location[1]] = '0'
            entities.Player.location[0] += dx
            entities.Player.location[1] += dy
            self.maps[entities.Player.location[0]][entities.Player.location[1]] = '2'
            return False
