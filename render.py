import pygame

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

WALL = 'src/env/light/wall.bmp'
GROUND = 'src/env/light/plitka1.bmp'
PLAYER = 'src/player/player00.bmp'
MOB = 'src/env/light/mob.bmp'
LADDER = 'src/env/light/ladder.bmp'
CHEST = 'src/env/light/chest.bmp'


def renderGame(sc, sector):
    x = 0
    y = 0
    img = 0
    for i in range(0, len(sector)):
        for j in range(0, len(sector[i])):
            if sector[i][j] == 0:
                img = pygame.image.load(GROUND)
            elif sector[i][j] == 1:
                img = pygame.image.load(WALL)
            elif sector[i][j] == 2:
                img = pygame.image.load(PLAYER)
            elif sector[i][j] == 3:
                img = pygame.image.load(MOB)
            elif sector[i][j] == 4:
                img = pygame.image.load(LADDER)
            elif sector[i][j] == 5:
                img = pygame.image.load(CHEST)
            sc.blit(img, img.get_rect(topleft=(x, y)))

            x += STEP
        x = 0
        y += STEP
