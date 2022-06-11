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