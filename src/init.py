from .gmglobal import *


class gmGame:
    def __init__(self):
        self.GameMode = None
        self.camX = 0
        self.camY = 0
        self.map = None
        self.gmPlayer = None
        self.uw = 500
        self.uh = 500
        self.debugMode = False
        self.actor = {"None": []}
        self.unusedActors = {}
        self.attacks = []
        self.health = 100
        self.hurtTimer = 0

    def loadSprite(self, _spr):
        self.frame = []
        sprSize = _spr.get_size()
        sprW = int(sprSize[0])
        sprH = int(sprSize[1])

        for i in range(0, int(sprH / 16)):
            for j in range(0, int(sprW / 16)):
                self.frame.append((j * 16, i * 16, 16, 16))

        return self.frame

    def run(self):
        if self.hurtTimer > 0:
            self.hurtTimer -= 1
        drawText(Font, 20, 20, str(round(clock.get_fps(), 1)))


class Map:
    def __init__(self, _a):
        self.actlast = 0
        self.actor = []
        self.actor_empty = {}
        self.a = _a


game = gmGame()

gmMap = Map(5)

solidTiles = [
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


def newActor(_type, _x, _y, _arr=None, _layer="None"):
    na = _type(_x, _y, _arr)
    na.id = gmMap.actlast
    game.actor[_layer].append(na)
    gmMap.actlast += 1


def runActors():
    for i in game.actor.values():
        for j in i:
            j.render()
            if game.debugMode == True:
                j.debug()
            j.run()
            # j.render()
