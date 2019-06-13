import random


class Entity(object):
    id = 0
    location = [0, 0]

    def __init__(self, id, level):
        self.id = id
        self.level = level


class Chest(Entity):
    count_of_items = 0
    items = []

    def __init__(self, id, level, x, y):
        super().__init__(id, level)
        self.count_of_items = random.randint(1, 4)
        self.location = [x, y]
        self.createChest()

    def createChest(self):
        i = 1
        while i < self.count_of_items:
            createArmor = random.randint(0, 1)
            createWeapon = random.randint(0, 1)
            createPostion = random.randint(0, 1)
            if createArmor == 0 and createPostion == 0 and createWeapon == 0:
                continue

            if createArmor == 1:
                if self.level < 4:
                    self.items.append({'armor': random.randint(1, 2)})
                elif self.level in range(4, 6):
                    self.items.append({'armor': random.randint(2, 4)})
                elif self.level > 6:
                    self.items.append({'armor': random.randint(3, 5)})

            if createWeapon == 1:
                if self.level < 4:
                    self.items.append({'weapon': random.randint(1, 2)})
                elif self.level in range(3, 7):
                    self.items.append({'weapon': random.randint(2, 4)})
                elif self.level > 6:
                    self.items.append({'weapon': random.randint(3, 5)})

            if createPostion == 1:
                self.items.append({'postion': True})
            i += 1


class Mob(Entity):
    hp = 0
    power = 0

    def __init__(self, id, level, x, y):
        super().__init__(id, level)
        self.hp = random.randint(self.level, self.level + 2)
        self.power = random.randint(self.level, self.level + 1)
        self.location = [x, y]


class Player(Entity):
    armor = 0
    armor_lvl = 0
    weapon_lvl = 0
    hp = 6
    power = 1
    inventory = []

    def __init__(self, id, level, location):
        super().__init__(id, level)
        self.location = location
