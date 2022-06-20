timer = 0
autocon = 300

class Testclass:
    def __init__(self, _x, _y, _arr=None):
        self.x = _x
        self.y = _y
        self.arr = _arr
        if self.arr != None:
            print(self.arr[0])

    def foo(self):
        print("testclass")

animation = {
    "events": [
        {
            "start": 200,
            "stop": 201,
            "autocon": {"right": False, "left": False, "up": False, "down": False},
            "anim": None,
            "function": 0,
            "spawn": [
                {
                    "entity": {"object": Testclass, "x": 400, "y": 200, "arr": None},
                },
                {"entity": {"object": Testclass, "x": 0, "y": 100, "arr": None}},
            ],
        },
        {
            "start": 200,
            "stop": 400,
            "autocon": {"right": False, "left": False, "up": False, "down": False},
            "anim": None,
            "function": 0,
            "spawn": [],
        },
        {
            "start": 400,
            "stop": 800,
            "autocon": {"right": False, "left": False, "up": False, "down": False},
            "anim": None,
            "function": 0,
            "spawn": [],
        },
    ]
}

class Attack:
    def __init__(self, _opponent, _timer=0):
        self.opponent = _opponent
        self.timer = 0

    def run(self):
        self.timer += 1
        for i in animation["events"]:
            if timer >= i["start"] and timer < i["stop"]:
                autocon = i["autocon"]
                anim = i["anim"]
                spawn = i["spawn"]
                for j in range(0, len(spawn)):
                    entity = spawn[j]["entity"]
                    object = entity["object"]
                    x = entity["x"]
                    y = entity["y"]
                    arr = entity["arr"]
                    # new_actor(object, x, y)
                    c = object(x, y, arr)
                    c.foo()

for i in animation["events"]:
    if timer >= i["start"] and timer < i["stop"]:
        autocon = i["autocon"]
        anim = i["anim"]
        spawn = i["spawn"]
        for j in range(0, len(spawn)):
            entity = spawn[j]["entity"]
            object = entity["object"]
            x = entity["x"]
            y = entity["y"]
            arr = entity["arr"]
            c = object(x, y, arr)
            c.foo()
