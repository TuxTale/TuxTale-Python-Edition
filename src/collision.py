from .actors import*

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
				return [True, i]
				