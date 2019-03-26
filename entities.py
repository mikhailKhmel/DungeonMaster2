import random
import math


class Entity(object):
    id = 0
    location = [0, 0]

    def __init__(self, id, level):
        self.id = id
        self.level = level


class Chest(Entity):
    count_of_items = 0

    def __init__(self, id, level):
        super().__init__(id, level)
        self.count_of_items = 10 - self.level

    def createChest(self, x, y):
        self.location = [x, y]
        tempChest = {'id': self.id, 'location': self.location}
        items = []
        for i in range(1, self.count_of_items):
            createArmor = random.randint(0, 1)
            createWeapon = random.randint(0, 1)
            createPostion = random.randint(0, 1)

            if createArmor == 1:
                if self.level < 4:
                    items.append({'armor': random.randint(1, 2)})
                elif self.level in range(4, 6):
                    items.append({'armor': random.randint(2, 4)})
                elif self.level > 6:
                    items.append({'armor': random.randint(3, 5)})

            if createWeapon == 1:
                if self.level < 4:
                    items.append({'weapon': random.randint(1, 2)})
                elif self.level in range(3, 7):
                    items.append({'weapon': random.randint(2, 4)})
                elif self.level > 6:
                    items.append({'weapon': random.randint(3, 5)})

            if createPostion == 1:
                items.append({'postion': True})
        return tempChest


class Mob(Entity):
    hp = 0
    power = 0

    def __init__(self, id, level, hp, power):
        super().__init__(id, level)
        self.hp = hp
        self.power = power
