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


