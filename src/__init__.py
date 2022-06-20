from .actors import *
from .init import *

def start_game():
    game.game_mode = game_play
    p = GameMap("res/map/test_for_PGE.json")
    p.draw_tiles()

    new_actor(Tux, 160, 160, None, "actorlayer")

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
        my_font.render(window, "Why do they call it oven, when you of in the cold food of out hot food eat the food?", (200, 200))
        pygame.display.update()