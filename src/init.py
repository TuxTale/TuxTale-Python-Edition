from .gmglobal import*

class gmGame():
	def __init__(self):
		self.GameMode = None
		self.camX = 0
		self.camY = 0
		self.map = None
		self.gmPlayer = None
		self.uw = 500
		self.uh = 500
		self.debugMode = False
	
	def run(self):
		if self.debugMode == True:
			for i in gmMap.actor:
				i.debug()

			drawText(Font, 20, 20, str(round(clock.get_fps(), 1)))

class Map():
	def __init__(self, _a):
		self.actlast = 0
		self.actor = []
		self.actor_empty = {}
		self.a = _a

game = gmGame()

gmMap = Map(5)

solidTiles = [18, 19, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41]

map_dict = [
	[ 0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  2],
	[ 7,  8,  8,  8,  8,  8,  8,  3,  8,  8,  8,  8,  8,  9],
	[ 7,  8,  3,  8,  8,  8,  3,  8,  8,  8, 10, 15, 15, 16],
	[ 7,  8,  8,  8,  8,  8,  8,  8, 10, 15, 16, 22, 22, 23],
	[ 7,  8,  8,  8,  8, 10, 15, 15, 16, 22, 23, 29, 29, 30],
	[14, 15, 15, 15, 15, 16, 22, 22, 23, 29, 30, 36, 36, 37],
	[28, 22, 22, 22, 22, 23, 29, 29, 30, 29, 37,  6,  6,  6],
	[28, 29, 29, 29, 29, 30, 29, 29, 37,  6,  6,  6,  6,  6],
	[35, 36, 36, 36, 36, 37,  6,  6,  6,  6,  6,  6,  6,  6]
]