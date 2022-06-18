from src.actors import *
from src.init import *


game.game_mode = gmPlay
p = gMap("res/map/test_for_PGE 2.json")
p.draw_tiles()

new_actor(Tux, 160, 160, None, "actorlayer")

game.cam_x = DisplayW / 2 - 16
game.cam_y = DisplayH / 2 - 16

new_actor(Slime, 300, 200, None, "actorlayer")

############### Testing ###############

############ Main game loop ##############


while running:
    clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    window.fill(BLACK)
    game.game_mode()
    game.run()

    pg.display.update()

