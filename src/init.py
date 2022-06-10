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
	
	def run(self):
		self.camX  = self.gmPlayer.shape.x - (DisplayW/2)
		self.camY = self.gmPlayer.shape.y - (DisplayH/2)
		#pass

game = gmGame()