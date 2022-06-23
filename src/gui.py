from .globals import *

def convert_to_centered(display, size, x, y):
    return (((display.get_width() // 2) - (size[0] // 2)) + x, ((display.get_height() // 2) - (size[1] // 2)) + y)

class GUIScreen:
    def __init__(self):
        self.widgets = []
    def handle_event(self, display, frame, event):
        for i in self.widgets:
            if i.handle_event(display, frame, event):
                return True
        
        return False
    def run(self, display):
        # Hide the original cursor

        pygame.mouse.set_visible(False)

        # Make a rect for the new cursor

        rect = sprite_cursor.get_rect()
        rect.center = pygame.mouse.get_pos()

        # Render widgets

        for i in self.widgets:
            i.run(display)

        # Show the new cursor on the screen
        
        display.blit(sprite_cursor, rect)

class GUIWidget:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def handle_event(self, display, event):
        pass
    def run(self, display):
        pass

class Button(GUIWidget):
    def __init__(self, x, y, image, image_dark):
        if image.get_rect().size != image_dark.get_rect().size:
            raise Exception("The normal Button image is not the same size as the dark Button image.")
        
        super().__init__(x, y)

        self.image = image
        self.image_dark = image_dark
        self.clicked = False
        #self.cooldown = 0
    
    def handle_event(self, display, frame, event):
        button_image = self.image
        button_size = button_image.get_rect().size
        button_position = convert_to_centered(display, button_size, self.x, self.y)
        button_rect = pygame.Rect(button_position[0], button_position[1], button_size[0], button_size[1])

        if button_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
            return True

        #if 0 > self.cooldown:
        #    self.cooldown = 0

        #if self.cooldown != 0:
        #    if frame > self.cooldown:
        #        self.cooldown = 0
        #    return False

        if button_rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
            #sound_menu_select.play()
            self.clicked = True
            #self.cooldown = frame + int(FPS * 0.7)
            return True
        
        return False

    def run(self, display):
        button_image = self.image
        button_size = button_image.get_rect().size
        button_position = convert_to_centered(display, button_size, self.x, self.y)
        button_rect = pygame.Rect(button_position[0], button_position[1], button_size[0], button_size[1])

        if self.clicked:
            button_image = self.image_dark

        display.blit(button_image, button_position)