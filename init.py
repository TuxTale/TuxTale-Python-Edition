from gmglobal import *

class Game:
    def __init__(self):
        self.game_mode = None
        self.cam_x = 0
        self.cam_y = 0
        self.map = None
        self.gm_player = None
        self.uw = 500
        self.uh = 500
        self.debugMode = False
        self.actor = dict()
        self.unusedActors = {}
        self.attacks = []
        self.health = 100
        self.hurtTimer = 0
        self.frame = []

    def load_sprite(self, _spr):
        sprite_size = _spr.get_size()
        sprite_w = int(sprite_size[0])
        sprite_h = int(sprite_size[1])

        for i in range(0, int(sprite_h / 16)):
            for j in range(0, int(sprite_w / 16)):
                self.frame.append((j * 16, i * 16, 16, 16))

        return self.frame

    def run(self):
        if self.hurtTimer > 0:
            self.hurtTimer -= 1
        
        draw_text(Font, 20, 20, str(round(clock.get_fps(), 1)))

class Map:
    def __init__(self, _a):
        self.actlast = 0
        self.actor = []
        self.actor_empty = {}
        self.a = _a

game = Game()

gmMap = Map(1)

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

def new_actor(_type, _x, _y, _arr=None, _layer="None"):
    na = _type(_x, _y, _arr)
    na.id = gmMap.actlast
    game.actor[_layer].append(na)
    gmMap.actlast += 1

def run_actors():
    for i in game.actor.values():
        for j in i:
            j.render()

            if game.debugMode:
                j.debug()
            
            j.run()
