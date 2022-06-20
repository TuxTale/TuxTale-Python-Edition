from src.actors import *
from src.init import *

# new_actor(Block, 20, 20, [sprite_marbel, [0]])

# new_actor(HorizontallyMovingBlock, 0, 150)
# new_actor(VerticallyMovingBlock, 100, 100)

game.game_mode = game_play
p = GameMap("res/map/test_for_PGE.json")
p.draw_tiles()

new_actor(Tux, 160, 160, None, "actorlayer")
# new_actor(Soul, 150, 150, None, "actorlayer")
# new_actor(Bullet, 140, 140, [(0.5, 0)], "actorlayer")
# new_actor(Bullet, 140, 140, [(-0.5, 0)], "actorlayer")

game.cam_x = display_w / 2 - 16
game.cam_y = display_H / 2 - 16

new_actor(Slime, 300, 250, None, "actorlayer")

# new_actor(Slime, 500, 400, None, "actorlayer")

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
