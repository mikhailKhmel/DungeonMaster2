import pygame
from entities import Player

STEP = 16
WINDOW_HEIGHT = 1024
WINDOW_WEIGHT = 1024

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
LADDER = 'src/env/light/ladder.bmp'
CHEST = 'src/env/light/chest.bmp'


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
    for i in range(startI, endI):
        for j in range(startJ, endJ):
            blitImg(sc, sector[i][j], x, y)
            x += STEP
        x = startX
        y += STEP


def renderGame(sc, sector, god_mode):
    if god_mode:
        x = 0
        y = 0
        for i in range(0, len(sector)):
            for j in range(0, len(sector[i])):
                blitImg(sc,sector[i][j],x,y)
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
                print('x=', x, '\ty=', y)
                renderLightZone(sc, sector, x, y, i, j)
            # else:
            #     blitImg(sc, sector[i][j], x, y)
            x += STEP
        x = 0
        y += STEP
