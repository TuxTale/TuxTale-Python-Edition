import pygame as pg
pg.font.init()
import math
from src.gmglobal import*
from src.actors import*
from src.gmplay import*
from src.controls import*
from src.init import*
import json

newActor(Tux, DisplayW/2 - 16, DisplayH/2 - 16)
for i in range(0, 10):
	newActor(Block, i * 16, 200)
for i in range(0, 10):
	newActor(Block, i*16, 232)

newActor(Block, 20, 20, [sprMarbel, [0]])

newActor(HorizontallyMovingBlock, 0, 150)
newActor(VerticallyMovingBlock, 100, 100)
	
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
	game.GameMode()
	game.run()
	Window.blit(pg.transform.scale(Canvas, Window.get_size()), (0, 0))
	pg.display.update()