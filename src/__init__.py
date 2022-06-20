from .actors import *
from .init import *
from .gui import *

def start_game():
    gui_screen = GUIScreen()

    gui_screen.widgets.append(Button(0, 0, sprite_button_fight, sprite_button_fight_dark))

    game.game_mode = game_play

    p = GameMap("res/map/test_for_PGE.json")
    p.draw_tiles()

    new_actor(Tux, 160, 160, None, "actorlayer")

    game.cam_x = display_w / 2 - 16
    game.cam_y = display_H / 2 - 16

    new_actor(Slime, 300, 250, None, "actorlayer")

    ############### Testing ###############

    ############ Main game loop ##############

    running = True
    frame = 0

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            keyboard.handle_event(event)

            if gui_screen.handle_event(window, frame, event):
                continue

            if event.type == pygame.QUIT:
                running = False

        window.fill(BLACK)

        pygame.mouse.set_visible(False)
        
        game.game_mode()
        game.run()

        if game.game_mode == battle_mode:
            gui_screen.widgets[0].x = (window.get_width() // 2) - gui_screen.widgets[0].image.get_rect().size[0]
            gui_screen.widgets[0].y = (window.get_height() // 2) - gui_screen.widgets[0].image.get_rect().size[1]

            gui_screen.run(window)
        
        my_font.render(window, "Why do they call it oven, when you of in the cold food of out hot food eat the food?", (200, 200))
        
        pygame.display.update()
        frame += 1