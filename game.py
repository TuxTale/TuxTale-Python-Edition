import pygame as pg
pg.font.init()
import math
from src.gmglobal import*
from src.actors import*
from src.gmplay import*
from src.controls import*
import json

newActor(Actor, 200, 200)
newActor(Actor, 200, 200)
newActor(Tux, 100, 100)

GameMode = gmPlay

############### Testing ###############

"""config = {}

config['up'] = '0'
config['down'] = '1'

def toJson(path, data):
	with open(path, 'w') as fp:
		json.dump(data, fp)

def rebindKeys(keys):
	toJson('config.json', config)

toJson('config.json', config)

f = open('config.json', "r")

Data = f.read()
f.close()

a = json.loads(Data)

print(a)"""

############ Main game loop ##############

while not Quit:
	clock.tick(FPS)	
	#Canvas.fill(BLACK)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			Quit = True
		if event.type == pg.VIDEORESIZE:
			pass
	
	key = pg.key.get_pressed()

	for event in pg.event.get():
		if event.type == pg.KEYDOWN:
			print("Is it working at all???")
			if key[config["key"]["left"]]:
				print("Test")
	#drawText(Font, 100, 100, "PYTHON")
	Canvas.fill(BLACK)
	GameMode()
	#drawText(Font, 50, 50, "Tuxtale w/ Pygame/Python")
	Window.blit(pg.transform.scale(Canvas, Window.get_size()), (0, 0))

	GameMode()
	pg.display.update()