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
newActor(Tux, DisplayW/2 - 16, DisplayH/2 - 16)
newActor(Block, 200, 200)

game.GameMode = gmPlay

############### Testing ###############

jsonWrite('config.json', config)

jsonRead('config.json')

############ Main game loop ##############

while not Quit:
	clock.tick(FPS)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			Quit = True
		if event.type == pg.VIDEORESIZE:
			pass
	
	for event in pg.event.get():
		if event.type == pg.QUIT:
			Quit = True

	Canvas.fill(BLACK)
	defControls()
	game.GameMode()
	game.run()
	Window.blit(pg.transform.scale(Canvas, Window.get_size()), (0, 0))
	pg.display.update()