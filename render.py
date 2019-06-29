import pygame


STEP = 32
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

LIGHT_WALL = 'src/env/light/new_wall.bmp'
LIGHT_GROUND = 'src/env/light/new_plitka.bmp'
DARK_WALL = 'src/env/dark/wall.bmp'
DARK_GROUND = 'src/env/dark/plitka1.bmp'

PLAYER = 'src/player/player00.bmp'
MOB = 'src/env/light/mob1.bmp'
RED = 'src/env/light/redMob.bmp'
LADDER = 'src/env/light/ladder.bmp'
CHEST = 'src/env/light/chest.bmp'

INV_BACK = 'src/inv/new_inv.png'
EMPTY_SLOT = 'src/inv/slot.png'
SELECTOR = 'src/inv/selector.png'

ARMOR_LVL1 = 'src/inv/armor_lvl1.png'
ARMOR_LVL2 = 'src/inv/armor_lvl2.png'
ARMOR_LVL3 = 'src/inv/armor_lvl3.png'
ARMOR_LVL4 = 'src/inv/armor_lvl4.png'
ARMOR_LVL5 = 'src/inv/armor_lvl5.png'

DISK_LVL1 = 'src/inv/disk_lvl1.png'
DISK_LVL2 = 'src/inv/disk_lvl2.png'
DISK_LVL3 = 'src/inv/disk_lvl3.png'
DISK_LVL4 = 'src/inv/disk_lvl4.png'
DISK_LVL5 = 'src/inv/disk_lvl5.png'

POTION = 'src/inv/potion.png'


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
    startY = y - STEP * 2

    x = startX
    y = startY

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

def renderOnlyInv(inv_sc,player):
    x=0
    y=0
    c=0
    for item in player.inventory:
        if item == '':
            img = pygame.image.load(EMPTY_SLOT)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'potion':
            img = pygame.image.load(POTION)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'disk_lvl1':
            img = pygame.image.load(DISK_LVL1)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'disk_lvl2':
            img = pygame.image.load(DISK_LVL2)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'disk_lvl3':
            img = pygame.image.load(DISK_LVL3)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'disk_lvl4':
            img = pygame.image.load(DISK_LVL4)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'disk_lvl5':
            img = pygame.image.load(DISK_LVL5)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'armor_lvl1':
            img = pygame.image.load(ARMOR_LVL1)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'armor_lvl2':
            img = pygame.image.load(ARMOR_LVL2)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'armor_lvl3':
            img = pygame.image.load(ARMOR_LVL3)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'armor_lvl4':
            img = pygame.image.load(ARMOR_LVL4)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        elif item == 'armor_lvl5':
            img = pygame.image.load(ARMOR_LVL5)
            img_rect = img.get_rect(topleft=(x, y))
            inv_sc.blit(img, img_rect)
            x+=54
        if c==2:
            x=0
            y+=53
        c+=1

def renderInv(sc, player,mode,pos):
    inv_sc = pygame.Surface((160,105))
    
    if mode:
        renderOnlyInv(inv_sc,player)
        surfSelect = pygame.Surface((54,53))
        surfSelect.set_alpha(200)
        
        if pos in [0,1,2]:
            y=0
            x=54*pos
        else:
            y=53
            x=54*(pos-3)

        img = pygame.image.load(SELECTOR)
        img_rect = img.get_rect(topleft=(0,0))
        surfSelect.blit(img, img_rect)
        inv_sc.blit(surfSelect,(x,y))
        
    else:
        renderOnlyInv(inv_sc,player)

    
    sc.blit(inv_sc, (800, 32*7))

def renderInfoAboutPlayer(sc,player,lvl,countofmobs):
    info_sc = pygame.Surface((160, 800))
    info_sc.fill((5, 67, 187))

    f = pygame.font.Font('src/Minecraftia.ttf', 16)

    text_hp = f.render("HP:  "+str(bin(player.hp))[1:], 0, (250, 162, 2))
    info_sc.blit(text_hp, (0,0))

    text_power = f.render("POWER:  "+str(bin(player.power+player.weapon_lvl))[1:], 0, (250, 162, 2))
    info_sc.blit(text_power, (0,32))

    text_armor = f.render("ARMOR:  "+str(bin(player.armor_lvl))[1:], 0, (250, 162, 2))
    info_sc.blit(text_armor, (0,64))

    wp_lvl = player.weapon_lvl
    if wp_lvl>5:
        wp_lvl-=5
    if wp_lvl == 0:
        img = pygame.image.load(EMPTY_SLOT)
        info_sc.blit(img,(16,32*4))
    elif wp_lvl == 1:
        img = pygame.image.load(DISK_LVL1)
        info_sc.blit(img,(16,32*4))
    elif wp_lvl == 2:
        img = pygame.image.load(DISK_LVL2)
        info_sc.blit(img,(16,32*4))
    elif wp_lvl == 3:
        img = pygame.image.load(DISK_LVL3)
        info_sc.blit(img,(16,32*4))
    elif wp_lvl == 4:
        img = pygame.image.load(DISK_LVL4)
        info_sc.blit(img,(16,32*4))
    elif wp_lvl == 5:
        img = pygame.image.load(DISK_LVL5)
        info_sc.blit(img,(16,32*4))

    arm_lvl = player.armor_lvl
    if arm_lvl>5:
        arm_lvl-=5
    if arm_lvl == 0:
        img = pygame.image.load(EMPTY_SLOT)
        info_sc.blit(img,(64+32,32*4))
    elif arm_lvl == 1:
        img = pygame.image.load(ARMOR_LVL1)
        info_sc.blit(img,(64+32,32*4))
    elif arm_lvl == 2:
        img = pygame.image.load(ARMOR_LVL2)
        info_sc.blit(img,(64+32,32*4))
    elif arm_lvl == 3:
        img = pygame.image.load(ARMOR_LVL3)
        info_sc.blit(img,(64+32,32*4))
    elif arm_lvl == 4:
        img = pygame.image.load(ARMOR_LVL4)
        info_sc.blit(img,(64+32,32*4))
    elif arm_lvl == 5:
        img = pygame.image.load(ARMOR_LVL5)
        info_sc.blit(img,(64+32,32*4))
    


    text_inv = f.render("INVENTORY: ",0,(250, 162, 2))
    info_sc.blit(text_inv, (0,32*6))

    text_inv = f.render("LVL: "+str(bin(lvl))[1:],0,(250, 162, 2))
    info_sc.blit(text_inv, (0,32*12))

    text_inv = f.render("MOBS: \n"+str(bin(countofmobs))[1:],0,(250, 162, 2))
    info_sc.blit(text_inv, (0,32*13))

    sc.blit(info_sc, (800,0))
    return

def renderGame(sc, sector, god_mode, player, lvl, countofmobs):
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
    renderInfoAboutPlayer(sc,player,lvl,countofmobs)
    renderInv(sc, player, False, -1)


def attackMob(sc, location):
    x = location[1] * STEP
    y = location[0] * STEP
    img = pygame.image.load(RED)
    img_rect = img.get_rect(topleft=(x, y))
    sc.blit(img, img_rect)
    return
