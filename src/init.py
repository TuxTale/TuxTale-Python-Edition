from .globals import *
from .utils import *


class Game:
    def __init__(self):
        self.game_mode = None
        self.cam_x = 0
        self.cam_y = 0
        self.map = None
        self.game_player = None
        self.uw = 500
        self.uh = 500
        self.debug_mode = False
        self.actor = {"None": []}
        self.unused_actors = {}
        self.attacks = []
        self.health = 100
        self.hurt_timer = 0
        self.frame = []

    def load_sprite(self, sprite):
        sprite_size = sprite.get_size()
        sprite_w = int(sprite_size[0])
        sprite_h = int(sprite_size[1])

        for i in range(0, int(sprite_h / 16)):
            for j in range(0, int(sprite_w / 16)):
                self.frame.append((j * 16, i * 16, 16, 16))

        return self.frame

    def run(self):
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        
        draw_text(game_font, 20, 20, str(round(clock.get_fps(), 1)), RED)


class Map:
    def __init__(self, _a):
        self.actlast = 0
        self.actor = []
        self.actor_empty = {}
        self.a = _a

def clip(surf, x, y, w, h):
    handle_surf = surf.copy()
    clipR = pygame.Rect(x, y, w, h)
    handle_surf.set_clip(clipR)
    image = surf.subsurface(handle_surf.get_clip())
    return image.copy()

class TheFont:
    def __init__(self, path):
        self.spacing = 1
        self.character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
        font_img = pygame.image.load(path).convert()
        print(font_img)
        current_char_width = 0
        self.characters = {}
        character_count = 0
        for x in range(font_img.get_width()):
            c = font_img.get_at((x,0))
            if c[0] == 127:
                char_img = clip(font_img, x - current_char_width, 0, current_char_width, font_img.get_height())
                print(char_img)
                self.characters[self.character_order[character_count]] = char_img.copy()
                character_count += 1
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.characters['A'].get_width()
        
    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.characters[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.characters[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing
            

my_font = TheFont('res/gfx/engine/uj font 2.png')

#my_font.render(window, "Hello World", (20, 20))

game = Game()

game_map = Map(5)

solid_tiles = [
    18,
    19,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
]

map_dict = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [7, 8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 9],
    [7, 8, 3, 8, 8, 8, 3, 8, 8, 8, 10, 15, 15, 16],
    [7, 8, 8, 8, 8, 8, 8, 8, 10, 15, 16, 22, 22, 23],
    [7, 8, 8, 8, 8, 10, 15, 15, 16, 22, 23, 29, 29, 30],
    [14, 15, 15, 15, 15, 16, 22, 22, 23, 29, 30, 36, 36, 37],
    [28, 22, 22, 22, 22, 23, 29, 29, 30, 29, 37, 6, 6, 6],
    [28, 29, 29, 29, 29, 30, 29, 29, 37, 6, 6, 6, 6, 6],
    [35, 36, 36, 36, 36, 37, 6, 6, 6, 6, 6, 6, 6, 6],
]

def new_actor(actor_type, x, y, arr=None, layer="None"):
    na = actor_type(x, y, arr)
    na.id = game_map.actlast
    game.actor[layer].append(na)
    game_map.actlast += 1

def run_actors():
    for i in game.actor.values():
        for j in i:
            j.render()
            
            if game.debug_mode:
                j.debug()
            
            j.run()
