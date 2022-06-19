import pygame

import json


pygame.font.init()

############ Sprite Sheets #############


def draw_sprite(spr, frame, x, y):
    window.blit(spr, (x, y), frame)


################ Colors #################

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

########### Window Properties ###########

display_w, display_H = 400, 240
Font = pygame.font.SysFont("comicsans", 40)
pygame.display.set_caption("Tuxtale [Python Edition]")

window = pygame.display.set_mode((display_w, display_H), pygame.RESIZABLE | pygame.SCALED)
FPS = 60
clock = pygame.time.Clock()
game_mode = None


########## Additional functions ##########


def draw_text(_font, _x, _y, text):
    text = _font.render(text, 1, RED)
    window.blit(text, (_x, _y))


def json_write(path, data):
    with open(path, "w") as fp:
        json.dump(data, fp)


def json_read(path):
    f = open(path, "r")
    Data = f.read()
    f.close()
    return json.loads(Data)


#################### Configurations ######################

config = {
    "key": {
        "up": pygame.K_UP,
        "down": pygame.K_DOWN,
        "left": pygame.K_LEFT,
        "right": pygame.K_RIGHT,
        "pause": pygame.K_ESCAPE,
        "accept": pygame.K_RETURN,
    }
}

RIGHT = config["key"]["right"]
LEFT = config["key"]["left"]
UP = config["key"]["up"]
DOWN = config["key"]["down"]
PAUSE = config["key"]["pause"]
ACCEPT = config["key"]["accept"]

######################## Game Data ########################

game_data = dict(map=None, posX=64, posY=64, cam_x=0, cam_y=0, dialogResponses={})

############# Sprite Sheets #############

sprite_tux = pygame.image.load("res/gfx/Tux/taletuxNL.png").convert_alpha()
sprite_block = pygame.image.load("res/gfx/tiles/block.png").convert_alpha()
sprite_marbel = pygame.image.load("res/gfx/tiles/blue_marbel 2.5d_v1.0.png").convert_alpha()
sprite_slime = pygame.image.load("res/gfx/tiles/slimes sheet.png").convert_alpha()
sprite_soul = pygame.image.load("res/gfx/Soul/soul.png").convert_alpha()
sprite_bullet = pygame.image.load("res/gfx/Soul/bullet.png").convert_alpha()
sprite_tree = pygame.image.load("res/gfx/tiles/big tree.png").convert_alpha()
