import pygame as pg
from .gmglobal import*
import json

def getcon_(control, state):
	pass

def jsonWrite(path, data):
	with open(path, 'w') as fp:
		json.dump(data, fp)
	
def jsonRead(path):
	f = open('config.json', "r")
	Data = f.read()
	f.close()
	return json.loads(Data)

def rebindKeys(keys):
	jsonWrite('config.json', config)

jsonWrite('config.json', config)

jsonRead('config.json')

def getcon(control, state):
	pass         	 #This is called by doing: if getcon("up", "press"): Execute code

state = {
	"keys": {},
	"left" : {"press": False, "hold": 0, "held": False},
	"right" : {"press": False, "hold": 0, "held": False},
	"up" : {"press": False, "hold": 0, "held": False},
	"down" : {"press": False, "hold": 0, "held": False},
	"pause" : {"press": False, "hold": 0, "held": False},
	"accept" : {"press": False, "hold": 0, "held": False}
}

def defControls():
	state["keys"] = pg.key.get_pressed()
	#for i in config["key"]:
	for i in config["key"]:
		if state["keys"][config["key"][i]]:
			if state[i]["held"] == False:
				state[i]["press"] = True
			else:
				state[i]["press"] = False
			state[i]["held"] = True
		else:
			state[i]["held"] = False
	
		print(state[i])

			
	
		


"""class defControls():
	def __init__(self):
		self.key = pg.key.get_pressed()
		self.hold = 0
		self.held = False
		self.press = False
	def run(self):
		self.key = pg.key.get_pressed()
		for i in self.key:
			if self.key[i] == True:
				self.hold+=1
			else:
				self.hold = 0
		
		if self.hold == 1:
			self.held = True
		
		if self.held == True:
			self.press = False
		
		if self.held == False:
			self.press = True


con = defControls()"""

