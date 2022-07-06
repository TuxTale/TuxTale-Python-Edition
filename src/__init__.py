from .actors import *
from .init import *

def start_game():
    p = GameMap("res/map/test_for_PGE.json")
    p.draw_tiles()
    game.game_mode = game_play

    #new_actor(Tux, 160, 160, None, "actorlayer")

    #game.cam_x = display_w / 2 - 16
    #game.cam_y = display_H / 2 - 16
    new_actor(Sprite, 600, 1100, [sprite_tree, 0, (46, 59)], "actorlayer")
    new_actor(Sprite, 700, 1050, [sprite_tree, 0, (46, 59)], "actorlayer")
    new_actor(NPC, 500, 500, [sprite_old_man], "actorlayer")
    new_actor(Sprite, 1000, 1000, [sprite_house, 0, (82, 121)], "MG")

    #new_actor(Slime, 300, 250, None, "actorlayer")

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

        if keyboard.is_released(UP):
            print("up")

        for i in game.text_boxes:
            i.box_function()
            print(i.dialogue_iterator)
        #print(game.text_boxes)
        #my_font.render(window, "My favourite song is Bohemian Rhapsody by Queen.", (0, 220))
        pygame.display.update()