import pygame as pg
pg.font.init()
import math
import json
import os

############ Sprite Sheets #############

def drawSprite(_spr, _frame, _x, _y):
	Canvas.blit(_spr, (_x, _y), _frame)

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
FPS = 60
clock = pg.time.Clock()
GameMode = None
Scale = 1

########## Additional functions ##########

def drawText(_font, _x, _y, text):
	text = _font.render(text, 0.5, RED)
	Canvas.blit(text, (_x, _y))

def jsonWrite(path, data):
	with open(path, 'w') as fp:
		json.dump(data, fp)
	
def jsonRead(path):
	f = open('config.json', "r")
	Data = f.read()
	f.close()
	return json.loads(Data)

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

######################## Game Data ########################

gmData = dict(
	map = None,
	posX = 64,
	posY = 64,
	camX = 0,
	camY = 0,
	dialogResponses = {}
)

############# Sprite Sheets #############

sprTux = pg.image.load("res/gfx/Tux/taletuxCL.png").convert()
sprBlock = pg.image.load("res/gfx/tiles/block.png").convert()



