import pygame
from entities import Player

STEP = 16
WINDOW_HEIGHT = 1024
WINDOW_WEIGHT = 1024

ARMOR_LOCATION = (96, 32)
WEAPON_LOCATION = (32, 32)

BAG = ((32, 96), (64, 96), (96, 96),
       (32, 128), (64, 128), (96, 128))

HEALTH = ((32, 224), (64, 224), (96, 224))
ARMOR = ((32, 288), (64, 288), (96, 288))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)

LIGHT_WALL = 'src/env/light/wall.bmp'
LIGHT_GROUND = 'src/env/light/plitka1.bmp'
DARK_WALL = 'src/env/dark/wall.bmp'
DARK_GROUND = 'src/env/dark/plitka1.bmp'

PLAYER = 'src/player/player00.bmp'
MOB = 'src/env/light/mob.bmp'
RED = 'src/env/light/redMob.bmp'
LADDER = 'src/env/light/ladder.bmp'
CHEST = 'src/env/light/chest.bmp'

INV_BACK = 'src/inv/new_inv.png'
ARMOR_LVL1 = 'src/inv/invarmour1.bmp'
ARMOR_LVL2 = 'src/inv/invarmour2.bmp'
WEAPON_LVL1 = 'src/inv/invweapon1.bmp'
WEAPON_LVL2 = 'src/inv/invweapon2.bmp'


def blitImg(sc, tpe, dx, dy):
    if tpe == '0':
        img = pygame.image.load(LIGHT_GROUND)
        img_rect = img.get_rect(topleft=(dx, dy))
        sc.blit(img, img_rect)
    elif tpe == '1':
        img = pygame.image.load(LIGHT_WALL)
        img_rect = img.get_rect(topleft=(dx, dy))
        sc.blit(img, img_rect)
    elif tpe == '2':
        img = pygame.image.load(PLAYER)
        img_rect = img.get_rect(topleft=(dx, dy))
        sc.blit(img, img_rect)
    elif tpe == '3':
        img = pygame.image.load(MOB)
        img_rect = img.get_rect(topleft=(dx, dy))
        sc.blit(img, img_rect)
    elif tpe == '4':
        img = pygame.image.load(LADDER)
        img_rect = img.get_rect(topleft=(dx, dy))
        sc.blit(img, img_rect)
    elif tpe == '5':
        img = pygame.image.load(CHEST)
        img_rect = img.get_rect(topleft=(dx, dy))
        sc.blit(img, img_rect)


def renderLightZone(sc, sector, x, y, i, j):
    startI = i - 2
    endI = startI + 5
    startJ = j - 2
    endJ = startJ + 5

    startX = x - STEP * 2
    endX = startX + 5 * STEP
    startY = y - STEP * 2
    endY = startY + 5 * STEP

    x = startX
    y = startY
    # for i in range(startI, endI):
    #     for j in range(startJ, endJ):
    #         blitImg(sc, sector[i][j], x, y)
    #         x += STEP
    #     x = startX
    #     y += STEP

    c = 0
    sector1 = [1, 2, 3]
    sector2 = [5, 10, 15]
    sector3 = [9, 14, 19]
    sector4 = [21, 22, 23]
    sector5 = [0, 4, 20, 24]
    for i in range(startI, endI):
        for j in range(startJ, endJ):
            if c in sector1 or c in sector2 or c in sector3 or c in sector4 or c in sector5:
                if c in sector1:
                    if sector[i + 1][j] == '1':
                        pygame.draw.rect(sc, (0, 0, 0), (x, y, x + STEP, y + STEP))
                    else:
                        blitImg(sc, sector[i][j], x, y)

                if c in sector2:
                    if sector[i][j + 1] == '1':
                        pygame.draw.rect(sc, (0, 0, 0), (x, y, x + STEP, y + STEP))
                    else:
                        blitImg(sc, sector[i][j], x, y)

                if c in sector3:
                    if sector[i][j - 1] == '1':
                        pygame.draw.rect(sc, (0, 0, 0), (x, y, x + STEP, y + STEP))
                    else:
                        blitImg(sc, sector[i][j], x, y)

                if c in sector4:
                    if sector[i - 1][j] == '1':
                        pygame.draw.rect(sc, (0, 0, 0), (x, y, x + STEP, y + STEP))
                    else:
                        blitImg(sc, sector[i][j], x, y)

                if c in sector5:
                    if c == 0:
                        if sector[i + 1][j + 1] == '1':
                            pygame.draw.rect(sc, (0, 0, 0), (x, y, x + STEP, y + STEP))
                        else:
                            blitImg(sc, sector[i][j], x, y)

                    if c == 4:
                        if sector[i + 1][j - 1] == '1':
                            pygame.draw.rect(sc, (0, 0, 0), (x, y, x + STEP, y + STEP))
                        else:
                            blitImg(sc, sector[i][j], x, y)

                    if c == 20:
                        if sector[i - 1][j + 1] == '1':
                            pygame.draw.rect(sc, (0, 0, 0), (x, y, x + STEP, y + STEP))
                        else:
                            blitImg(sc, sector[i][j], x, y)

                    if c == 24:
                        if sector[i - 1][j - 1] == '1':
                            pygame.draw.rect(sc, (0, 0, 0), (x, y, x + STEP, y + STEP))
                        else:
                            blitImg(sc, sector[i][j], x, y)
            else:
                blitImg(sc, sector[i][j], x, y)
            c += 1
            x += STEP
        x = startX
        y += STEP


def renderInv(sc, player):
    inv_sc = pygame.Surface((160, 383))

    img = pygame.image.load(INV_BACK)
    img_rect = img.get_rect(topleft=(0, 0))
    inv_sc.blit(img, img_rect)


    sc.blit(inv_sc, (800, 0))


def renderGame(sc, sector, god_mode, player):
    if god_mode:
        x = 0
        y = 0
        for i in range(0, len(sector)):
            for j in range(0, len(sector[i])):
                blitImg(sc, sector[i][j], x, y)
                x += STEP
            x = 0
            y += STEP
        return
    x = 0
    y = 0
    sc.fill((0, 0, 0))
    for i in range(0, len(sector)):
        for j in range(0, len(sector[i])):
            if sector[i][j] == '2':
                # print('x=', x, '\ty=', y)
                renderLightZone(sc, sector, x, y, i, j)
            # else:
            #     blitImg(sc, sector[i][j], x, y)
            x += STEP
        x = 0
        y += STEP

    renderInv(sc, player)


def attackMob(sc, location):
    x = location[1] * STEP
    y = location[0] * STEP
    img = pygame.image.load(RED)
    img_rect = img.get_rect(topleft=(x, y))
    sc.blit(img, img_rect)
    return
