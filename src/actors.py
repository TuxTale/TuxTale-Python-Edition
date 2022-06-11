import pygame as pg
pg.font.init()
import math
from .gmglobal import*
from .controls import*
from .init import*
import sys

class Physactor():
	def __init__(self, _x, _y):
		self.x = _x
		self.y = _y
		self.w = 0
		self.h = 0
		self.xprev = _x
		self.yprev = _y


	def run(self):
		pass
	
	def render(self):
		pass

class Actor():
	id = 0
	def __init__(self, _x, _y, _arr = None):
		self.x = _x
		self.y = _y
		self.h = 1
		self.w = 1
		self.xspeed = 0
		self.yspeed = 0
		self.arr = _arr
		self.anim = None
		self.frame = None
		self.shape = None
		self.frameIndex = 0
		self.id = Actor.id
		self.frame = []
		self.shape = pg.Rect(self.x, self.y, self.h, self.w)
		self.solid = False
		if(not self.arr):
			return
		if self.arr.len() == 1:
			self.spriteSheet = self.arr[0]
	
	def loadSprite(self, _spr):
		self.frame = []
		sprSize = _spr.get_size()
		sprW = int(sprSize[0])
		sprH = int(sprSize[1])

		for i in range(0, int(sprH/16)):
			for j in range(0, int(sprW/16)):
				self.frame.append((j*16, i*16, 16, 16))
	
	def collision(self, _direction):
		for i in gmMap.actor:
			if i._typeof() == "Block":
				if i.shape.colliderect(self.shape):
					if i.solid == True:
						if _direction == "horizontal":
							if self.xspeed > 0:
								self.shape.right = i.shape.left
							
							if self.xspeed < 0:
								self.shape.left = i.shape.right
						
						if _direction == "vertical":
							if self.yspeed > 0:
								self.shape.bottom = i.shape.top

							if self.yspeed < 0:
								self.shape.top = i.shape.bottom

			

	def run(self):
		pass
	
	def render(self):
		pg.draw.rect(Canvas, (255, 255, 255), (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h))

	def destructor():
		pass

	def _typeof(self):
		return "Actor"

def runActors():
	for i in gmMap.actor:
		i.run()

def renderActors():
	for i in gmMap.actor:
		i.render()
		
def newActor(_type, _x, _y, _arr = None):
	na = _type(_x, _y, _arr)
	na.id = gmMap.actlast
	gmMap.actor.append(na)
	gmMap.actlast += 1

# Moving block
class MovingBlock(Actor):
	def __init__(self, _x, _y, _arr = None):
		super().__init__(_x, _y, _arr = None)
		self.originalX = _x
		self.x = _x
		self.y = _y
		self.w = 16
		self.h = 16
		self.arr = _arr
		self.shape = pg.Rect(self.x, self.y, self.h, self.w)
		self.loadSprite(sprBlock)
		self.solid = True
		self.color = (200, 200, 200)
		self.frameCount = 0
		if(not self.arr):
			return
		if self.arr.len() == 1:
			self.spriteSheet = self.arr[0]
			self.loadSprite(self.spriteSheet)
	
	def run(self):
		self.frameCount += 1
	
		self.x = self.originalX + math.sin(self.frameCount / 25) * 32
	
		self.shape.x = self.x
		self.shape.y = self.y
	
	def render(self):
		drawSprite(sprBlock, self.frame[0], self.x - game.camX, self.y - game.camY)
		#pg.draw.rect(Canvas, self.color, (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h), 0)
		
	def _typeof(self):
		return "Block"
	
	def debug(self):
		pg.draw.rect(Canvas, self.color, (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h), 0)

	
class Block(Actor):
	def __init__(self, _x, _y, _arr = None):
		super().__init__(_x, _y, _arr = None)
		self.x = _x
		self.y = _y
		self.w = 16
		self.h = 16
		self.arr = _arr
		self.shape = pg.Rect(self.x, self.y, self.h, self.w)
		self.loadSprite(sprBlock)
		self.solid = True
		self.color = (200, 200, 200)
		if(not self.arr):
			return
		if self.arr.len() == 1:
			self.spriteSheet = self.arr[0]
			self.loadSprite(self.spriteSheet)
	
	def run(self):
		self.shape.x = self.x
		self.shape.y = self.y
	
	def render(self):
		drawSprite(sprBlock, self.frame[0], self.x - game.camX, self.y - game.camY)
		#pg.draw.rect(Canvas, self.color, (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h), 0)
		
	def _typeof(self):
		return "Block"
	
	def debug(self):
		pg.draw.rect(Canvas, self.color, (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h), 0)

		
class Tux(Actor):
	def __init__(self, _x, _y, _arr = None):
		super().__init__(_x, _y, _arr = None)
		self.x = _x
		self.y = _y
		self.w = 16
		self.h = 16
		self.arr = _arr
		self.frame = []
		self.walkRight = [0.0, 3.0]
		self.walkUp = [4.0, 7.0]
		self.walkDown = [8.0, 11.0]
		self.walkLeft = [12.0, 15.0]
		self.standRight = [0]
		self.standLeft = [12]
		self.standUp = [4]
		self.standDown = [8]
		self.anim = self.walkRight
		self.standStillAnim = self.standRight
		self.xspeed = 0
		self.yspeed = 0
		self.autocon = False
		self.idle = False
		self.stepCount = 0
		self.shape = pg.Rect(self.x, self.y, self.h, self.w)
		self.loadSprite(sprTux)
		self.solid = False
		self.color = (0, 255, 0)
		game.gmPlayer = self
		if not _arr:
			return

	def run(self):

		if not getcon("right", "held") or not getcon("left", "held"):
			self.xspeed = 0
		
		if not getcon("up", "held") or not getcon("down", "held"):
			self.yspeed = 0

		if getcon("right", "held"):
			self.xspeed = 1
			self.anim = self.walkRight
			self.standStillAnim = self.standRight
		
		if getcon("left", "held"):
			self.xspeed = -1
			self.anim = self.walkLeft
			self.standStillAnim = self.standLeft

		if getcon("up", "held"):
			self.yspeed = -1
			self.anim = self.walkUp
			self.standStillAnim = self.standUp
		
		if getcon("down", "held"):
			self.yspeed = 1
			self.anim = self.walkDown
			self.standStillAnim = self.standDown
		
		if getcon("right", "press") or getcon("left", "press") or getcon("up", "press") or getcon("down", "press"):
			self.stepCount += 1
			if self.stepCount % 2 == 0:
				self.frameIndex = 1
			else:
				self.frameIndex = 3

		if self.xspeed == 0 and self.yspeed == 0:
			self.anim = self.standStillAnim


		self.shape.x += self.xspeed
		self.x += self.xspeed
		self.collision("horizontal")
		self.shape.y += self.yspeed
		self.y += self.yspeed
		self.collision("vertical")

		self.frameIndex += 0.14
	
	def render(self):
		drawSprite(sprTux, self.frame[int(self.anim[0]) + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))], self.shape.x - game.camX, self.shape.y - game.camY)
	
	def debug(self):
		pg.draw.rect(Canvas, self.color, (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h), 0)




