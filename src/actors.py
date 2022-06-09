import pygame as pg
pg.font.init()
import math
from .gmglobal import*
from .controls import*
from .init import*

class Physactor():
	def __init__(self, _x, _y):
		self.x = _x
		self.y = _y
		self.w = 0
		self.h = 0
		self.xprev = _x
		self.yprev = _y


	def collision(self, _x, _y):
		for i in gmMap.actor:
			if abs(_x - i.x) < self.w + i.w and abs(_y - i.y) < self.h + i.h:
				return True

class Map():
	def __init__(self, _a):
		self.actlast = 0
		self.actor = []
		self.actor_empty = {}
		self.a = _a

gmMap = Map(5)

class Actor():
	id = 0
	def __init__(self, _x, _y, _arr = None):
		self.x = _x
		self.y = _y
		self.h = 0
		self.w = 0
		self.arr = _arr
		self.anim = None
		self.frame = None
		self.shape = None
		self.frameIndex = 0
		self.id = Actor.id
		self.frame = []
		if(not self.arr):
			return
		if self.arr.len() == 1:
			pass
	
	def loadSprite(self, _spr):
		sprSize = _spr.get_size()
		sprW = int(sprSize[0])
		sprH = int(sprSize[1])

		for i in range(0, int(sprH/16)):
			for j in range(0, int(sprW/16)):
				self.frame.append((j*16, i*16, 16, 16))
	
	def collision(self, _x, _y):
		for i in gmMap.actor:
			if i._typeof() == "Block":
				if abs(_x - i.x) < self.w + i.w and abs(_y - i.y) < self.h + i.h:
					
					return True

	def run(self):
		pass

	def destructor():
		pass

	def _typeof(self):
		return "Actor"

def runActors():
	for i in gmMap.actor:
		i.run()

def newActor(_type, _x, _y, _arr = None):
	na = _type(_x, _y, _arr)
	na.id = gmMap.actlast
	gmMap.actor.append(na)
	##gmMap.actor[gmMap.actlast] = na
	gmMap.actlast += 1

class Block(Actor):
	def __init__(self, _x, _y, _arr = None):
		super().__init__(_x, _y, _arr = None)
		self.x = _x
		self.y = _y
		self.w = 8
		self.h = 8
		self.arr = _arr
		self.loadSprite(sprBlock)
	
	def run(self):
		drawSprite(sprBlock, self.frame[0], self.x - game.camX, self.y - game.camY)
	
	def _typeof(self):
		return "Block"

		
class Tux(Actor):
	def __init__(self, _x, _y, _arr = None):
		super().__init__(_x, _y, _arr = None)
		self.x = _x
		self.y = _y
		self.w = 8
		self.h = 8
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
		self.stepCount = 0
		self.loadSprite(sprTux)
		game.gmPlayer = self
		if not _arr:
			return

	def run(self):

		if not getcon("right", "held") or not getcon("left", "held"):
			self.xspeed = 0
			self.anim = self.standStillAnim
		
		if not getcon("up", "held") or not getcon("down", "held"):
			self.yspeed = 0
			self.anim = self.standStillAnim

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
			#pass

		if self.collision(self.x + self.xspeed, self.y):
			self.xspeed = 0
			print("xspeed = 0")
		
		if self.collision(self.x, self.y + self.yspeed):
			self.yspeed = 0
			print("yspeed = 0")


		self.x += self.xspeed
		self.y += self.yspeed

		self.frameIndex += 0.14
		drawSprite(sprTux, self.frame[int(self.anim[0]) + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))], self.x - game.camX, self.y - game.camY)



