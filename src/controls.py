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
