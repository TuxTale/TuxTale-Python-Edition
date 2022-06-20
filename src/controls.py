from .globals import *
import time

state = {
    "keys": {},
    "left": {"press": False, "hold": 0, "held": False},
    "right": {"press": False, "hold": 0, "held": False},
    "up": {"press": False, "hold": 0, "held": False},
    "down": {"press": False, "hold": 0, "held": False},
    "pause": {"press": False, "hold": 0, "held": False},
    "accept": {"press": False, "hold": 0, "held": False},
}

def get_control(_control, _state):
    state["keys"] = pygame.key.get_pressed()
    for i in config["key"]:
        if state["keys"][config["key"][i]]:
            if not state[i]["held"]:
                state[i]["press"] = True
            else:
                state[i]["press"] = False
            
            state[i]["held"] = True
        else:
            state[i]["held"] = False

    if state[_control][_state]:
        return True


def def_controls():
    state["keys"] = pygame.key.get_pressed()

    for i in config["key"]:
        if state["keys"][config["key"][i]]:
            if not state[i]["held"]:
                state[i]["press"] = True
            else:
                state[i]["press"] = False
            
            state[i]["held"] = True
        else:
            state[i]["held"] = False


class Keyboard:
    def __init__(self):
        self.keys = {}

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            self.keys[event.key] = time.time()
        elif event.type == pygame.KEYUP:
            self.keys[event.key] = False

    def is_held(self, key: int) -> bool:
        """check if the key is currently pressed"""

        return key in self.keys and self.keys[key]

    def is_pressed(self, key: int) -> bool:
        hold_time = self.hold_time(key)
        if hold_time is not None:
            if hold_time <= 1 / 60:
                return key in self.keys and self.keys[key]

    def press_time(self, key: int) -> [float]:
        """check the time the held key was pressed"""

        if key not in self.keys or not self.keys[key]:
            return
        return self.keys[key]

    def hold_time(self, key: int) -> float:
        """"check for how long held key is pressed"""
								
        if key in self.keys:
            return time.time() - self.keys[key]


keyboard = Keyboard()
