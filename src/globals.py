import pygame

pygame.init()

################ Colors #################

RED = (255, 0, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

########### Window Properties ###########

display_w, display_H = 400, 240
game_font = pygame.font.SysFont("comicsans", 40)
pygame.display.set_caption("Tuxtale [Python Edition]")

window = pygame.display.set_mode((display_w, display_H), pygame.RESIZABLE | pygame.SCALED)
FPS = 60
clock = pygame.time.Clock()
game_mode = None

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

sprite_tux = pygame.image.load("res/gfx/Tux/taletuxCL.png").convert_alpha()
sprite_block = pygame.image.load("res/gfx/tiles/block.png").convert_alpha()
sprite_marbel = pygame.image.load("res/gfx/tiles/blue_marbel 2.5d_v1.0.png").convert_alpha()
sprite_slime = pygame.image.load("res/gfx/tiles/slimes sheet.png").convert_alpha()
sprite_soul = pygame.image.load("res/gfx/Soul/soul.png").convert_alpha()
sprite_bullet = pygame.image.load("res/gfx/Soul/bullet.png").convert_alpha()
sprite_tree = pygame.image.load("res/gfx/tiles/big tree.png").convert_alpha()

######################## GUI Sprites ########################

sprite_cursor = pygame.image.load("res/gfx/engine/cursor.png").convert_alpha()
sprite_button_defend = pygame.image.load("res/gfx/Battle/button-defend.png").convert_alpha()
sprite_button_defend_dark = pygame.image.load("res/gfx/Battle/button-defend-dark.png").convert_alpha()
sprite_button_fight = pygame.image.load("res/gfx/Battle/button-fight.png").convert_alpha()
sprite_button_fight_dark = pygame.image.load("res/gfx/Battle/button-fight-dark.png").convert_alpha()
sprite_button_end = pygame.image.load("res/gfx/Battle/button-end.png").convert_alpha()
sprite_button_end_dark = pygame.image.load("res/gfx/Battle/button-end-dark.png").convert_alpha()

######################## GUI Sounds ########################

# TODO: This sound is a placeholder (and I disabled it), replace it with something else
#sound_menu_select = pygame.mixer.Sound("res/sfx/menu-select.ogg")
