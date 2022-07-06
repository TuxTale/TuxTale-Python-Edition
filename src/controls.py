from .globals import *
import time

class Keyboard:
    def __init__(self):
        self.keys = {"held": {}, "pressed": {}, "released": {}}

    def handle_event(self, event: pygame.event) -> None:
        if event.type == pygame.KEYDOWN:
            self.keys["held"][event.key] = time.time()
            self.keys["pressed"][event.key] = time.time()
        elif event.type == pygame.KEYUP:
            self.keys["held"][event.key] = False
            self.keys["released"][event.key] = time.time()

    def is_held(self, key: int) -> bool:
        """check if the key is currently pressed"""

        return key in self.keys["held"] and self.keys["held"][key]

    def is_released(self, key: int) -> bool:
        status_time = self.status_time("released", key)
        if status_time is not None:
            if status_time <= 1 / 60:
                return key in self.keys["released"] and self.keys["released"][key]

    def is_pressed(self, key: int) -> bool:
        status_time = self.status_time("pressed", key)
        if status_time is not None:
            if status_time <= 1 / 60:
                return key in self.keys["pressed"] and self.keys["pressed"][key]

    def press_time(self, key: int) -> [float]:
        """check the time the held key was pressed"""

        if key not in self.keys or not self.keys[key]:
            return
        return self.keys[key]

    def status_time(self,status, key: int) -> float:
        """"check for how long held key is pressed"""
								
        if key in self.keys[status]:
            return time.time() - self.keys[status][key]


keyboard = Keyboard()
