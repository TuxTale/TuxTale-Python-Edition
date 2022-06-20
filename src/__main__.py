from .actors import *
from .init import *

game.game_mode = game_play
p = gMap("res/map/test_for_PGE.json")
p.draw_tiles()

new_actor(Tux, 500, 500, None, "actorlayer")

new_actor(Sprite, 600, 1100, [sprite_tree, 0, (46, 59)], "actorlayer")
new_actor(Sprite, 700, 1050, [sprite_tree, 0, (46, 59)], "actorlayer")

game.cam_x = display_w / 2 - 16
game.cam_y = display_H / 2 - 16

############### Testing ###############

############ Main game loop ##############

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        keyboard.handle_event(event)
        if event.type == pygame.QUIT:
            running = False

    window.fill(BLACK)
    game.game_mode()
    game.run()

    pygame.display.update()
