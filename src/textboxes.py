from .init import game, my_font
from .controls import keyboard
from .globals import*

Dialogue = {
    "0":{
        "speaker": "Jon",
        "type": "text",
        "text": "Hello."
    },
    "1":{
        "speaker": "Jon",
        "type": "text",
        "text": "You seem like you need some items."
    },
    "2":{
        "speaker": "Jon",
        "type": "question",
        "question": "What item would you like?",
        "answers":{
            "0":{
                "text": "Potato",
                "$":lambda _: print("lambda!")
            },
            "1":{
                "text": "Bean",
                "$":lambda _: new_textbox(20, 20, Dialogue)
            },
            "2":{
                "text": "Frog pet",
                "$":"I would like to have code here representing the player being given the item"
            }
        }
        
    }
}

class TextBox:
    def __init__(self, _x, _y, _dialogue):
        self.x = _x
        self.y = _y
        #self.file = _file
        self.dialogue = _dialogue
        self.speaker = None
        self.current_text = None
        self.menu_x = 0
        self.menu_y = 0
        self.arrow = 0
        self.dialogue_iterator = -1
        self.box_function = self.load_dialogue
    
    def load_dialogue(self):
        if self.dialogue_iterator != -1 and self.dialogue_iterator != len(self.dialogue):
            if self.dialogue[str(self.dialogue_iterator)]["type"] == "text":
                my_font.render(window, self.dialogue[str(self.dialogue_iterator)]["text"], (self.x, self.y))
            if self.dialogue[str(self.dialogue_iterator)]["type"] == "question":
                self.box_function = self.textbox_menu
        if keyboard.is_pressed(ACCEPT):
            if self.dialogue_iterator != -1:
                if self.dialogue[str(self.dialogue_iterator)] == self.dialogue[str(len(self.dialogue)-1)]:
                    game.text_boxes.remove(self)
            self.dialogue_iterator += 1
    
    def textbox_menu(self):
        my_font.render(window, self.dialogue[str(self.dialogue_iterator)]["question"], (self.x, self.y))
        for i, (a, b) in enumerate(self.dialogue[str(self.dialogue_iterator)]["answers"].items()):
            length = len(self.dialogue[str(self.dialogue_iterator)]["answers"])
            my_font.render(window, b["text"], (self.x + 16, self.y + 16*(i + 1)))
            if self.arrow == i:
                
                my_font.render(window, ">", (self.x, self.y + 16*(i + 1)))
        if keyboard.is_pressed(DOWN):
            if self.arrow == length-1:
                self.arrow = 0
            else:
                self.arrow += 1
        if keyboard.is_pressed(UP):
            if self.arrow == 0:
                self.arrow = length-1
            else:
                self.arrow -=1
        if keyboard.is_pressed(ACCEPT):
            self.dialogue[str(self.dialogue_iterator)]["answers"][str(self.arrow)]["$"](self)
    
    def end_convo(self):
        pass
    def next_convo(self):
        pass

def new_textbox(_x, _y, _dialogue):
    game.text_boxes = []
    game.text_boxes.append(TextBox(_x, _y, _dialogue))
    game.text_boxes[-1].dialogue_iterator = 0
    print(game.text_boxes)