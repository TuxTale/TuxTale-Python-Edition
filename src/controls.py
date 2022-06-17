from .gmglobal import *


def getcon(control, state):
    pass  # This is called by doing: if getcon("up", "press"): Execute code


state = {
    "keys": {},
    "left": {"press": False, "hold": 0, "held": False},
    "right": {"press": False, "hold": 0, "held": False},
    "up": {"press": False, "hold": 0, "held": False},
    "down": {"press": False, "hold": 0, "held": False},
    "pause": {"press": False, "hold": 0, "held": False},
    "accept": {"press": False, "hold": 0, "held": False},
}


def getcon(_control, _state):
    state["keys"] = pg.key.get_pressed()
    # for i in config["key"]:
    for i in config["key"]:
        if state["keys"][config["key"][i]]:
            if state[i]["held"] == False:
                state[i]["press"] = True
            else:
                state[i]["press"] = False
            state[i]["held"] = True
        else:
            state[i]["held"] = False

    if state[_control][_state] == True:
        return True


def defControls():
    state["keys"] = pg.key.get_pressed()
    # for i in config["key"]:
    for i in config["key"]:
        if state["keys"][config["key"][i]]:
            if state[i]["held"] == False:
                state[i]["press"] = True
            else:
                state[i]["press"] = False
            state[i]["held"] = True
        else:
            state[i]["held"] = False

import time

class Keyboard:
	def __init__(self):
		self.keys = {}

	def handle_event(self, event:int) -> None:
		if event.type == pg.KEYDOWN:
			self.keys[event.key] = time.time()
		elif event.type == pg.KEYUP:
			self.keys[event.key] = False
	
	def is_held(self, key:int) -> bool:
		# check if the key is currently pressed
		return key in self.keys and self.keys[key] is not False

	def is_pressed(self, key:int) -> bool:
		hold_time = self.hold_time(key)
		if hold_time != None:
			if hold_time <= 1/60:
				return key in self.keys and self.keys[key] is not False
	
	def press_time(self, key:int) -> float:
		# check the time the held key was pressed
		if key not in self.keys or self.keys[key] is False:
			return None
		return self.keys[key]
	
	def hold_time(self, key:int) -> float:
		# check for how long held key is pressed
		if key in self.keys:
			return time.time() - self.keys[key]

keyboard = Keyboard()
