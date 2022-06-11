class dog():
	def __init__(self, _arr = None):
		self.arr = _arr
	
class puppy(dog):
	def _init__(self, _arr = None):
		super.__init__(_arr = None)
		self.arr = _arr

list = []

def spawn(_arr = None):
	q = puppy(_arr)
	list.append(q)

spawn(["bark!"])

for i in list:
	print(i.arr) #Prints ["bark"!]