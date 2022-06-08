import pygame as pg
pg.font.init()
import math

############ Sprite Sheets #############

sprTux = pg.image.load("res/gfx/Tux/taletuxCL.png")

def drawSprite(_spr, _frame, _x, _y):
	Canvas.blit(_spr, (_x, _y), _frame)

"""def loadSprite(_spr):
	sprSize = _spr.get_size()
	sprW = int(sprSize[0])
	sprH = int(sprSize[1])

	for i in range(0, int(sprH/16)):
		for j in range(0, int(sprW/16)):
			frame.append((j*16, i*16, 16, 16))"""

############# Sprite Sheets #############

sprTux = pg.image.load("res/gfx/Tux/taletuxCL.png")

################ Colors #################

RED = (255, 0, 0)
BLACK = (0, 0, 0)

########### Window Properties ###########

Quit = False
DisplayW, DisplayH = 400, 240
Font = pg.font.SysFont("comicsans", 20)
pg.display.set_caption("Tuxtale [Python Edition]")

Canvas = pg.Surface((DisplayW, DisplayH))
Window = pg.display.set_mode((DisplayW, DisplayH), pg.RESIZABLE)
FPS = 50
clock = pg.time.Clock()
GameMode = None
Scale = 1

########## Additional functions ##########

def drawText(_font, _x, _y, text):
	text = _font.render(text, 0.5, RED)
	Canvas.blit(text, (_x, _y))

#################### Configurations ######################

config = {
	"key" : {
		"up" : pg.K_UP,
		"down" : pg.K_DOWN,
		"left" : pg.K_LEFT,
		"right" : pg.K_RIGHT,
		"pause" : pg.K_ESCAPE,
		"accept" : pg.K_RETURN
	}
}