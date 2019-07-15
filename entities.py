import random


class Entity(object):
    id = 0
    location = [0, 0]

    def __init__(self, id):
        self.id = id


class Chest(Entity):

    def __init__(self, id, x, y):
        super().__init__(id)

        self.location = [x, y]


class Mob(Entity):
    hp = 0
    power = 0

    def __init__(self, id, level, x, y):
        super().__init__(id)
        self.power = random.randint(level, level + 2)
        self.hp = random.randint(level, level + 1)
        self.location = [x, y]


class Player(Entity):
    armor_lvl = 0
    weapon_lvl = 0
    hp = 10
    power = 1
    inventory = ['', '', '',
                 '', '', '']
    view_location = []

    def __init__(self, id, location, view_location):
        super().__init__(id)
        self.location = location
        self.view_location = view_location
