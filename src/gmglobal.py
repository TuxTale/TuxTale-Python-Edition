import pygame as pg

pg.font.init()

import json


############ Sprite Sheets #############


def drawSprite(_spr, _frame, _x, _y):
    window.blit(_spr, (_x, _y), _frame)


################ Colors #################

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

########### Window Properties ###########

running = True
DisplayW, DisplayH = 400, 240
Font = pg.font.SysFont("comicsans", 40)
pg.display.set_caption("Tuxtale [Python Edition]")

window = pg.display.set_mode((DisplayW, DisplayH), pg.RESIZABLE | pg.SCALED)
FPS = 60
clock = pg.time.Clock()
game_mode = None


########## Additional functions ##########


def draw_text(_font, _x, _y, text):
    text = _font.render(text, 1, RED)
    window.blit(text, (_x, _y))


def json_write(path, data):
    json.dump(data, open(path, "w"))


def json_read(path):
    return json.loads(open(path, "r").read())


#################### Configurations ######################

config = {
    "key": {
        "up": pg.K_UP,
        "down": pg.K_DOWN,
        "left": pg.K_LEFT,
        "right": pg.K_RIGHT,
        "pause": pg.K_ESCAPE,
        "accept": pg.K_RETURN,
    }
}

######################## Game Data ########################

gmData = dict(map=None, posX=64, posY=64, cam_x=0, cam_y=0, dialogResponses={})

############# Sprite Sheets #############

sprite_tux = pg.image.load("res/gfx/Tux/taletuxCL.png").convert_alpha()
sprite_block = pg.image.load("res/gfx/tiles/block.png").convert_alpha()
sprite_marbel = pg.image.load("res/gfx/tiles/blue_marbel 2.5d_v1.0.png").convert_alpha()
sprite_slime = pg.image.load("res/gfx/tiles/slimes sheet.png").convert_alpha()
sprite_soul = pg.image.load("res/gfx/Soul/soul.png").convert_alpha()
sprite_bullet = pg.image.load("res/gfx/Soul/bullet.png").convert_alpha()
