from src.actors import *
from src.init import *

# newActor(Block, 20, 20, [sprMarbel, [0]])

# newActor(HorizontallyMovingBlock, 0, 150)
# newActor(VerticallyMovingBlock, 100, 100)

game.GameMode = gmPlay
p = gMap("res/map/test_for_PGE.json")
p.drawTiles()

newActor(Tux, 160, 160, None, "actorlayer")
# newActor(Soul, 150, 150, None, "actorlayer")
# newActor(Bullet, 140, 140, [(0.5, 0)], "actorlayer")
# newActor(Bullet, 140, 140, [(-0.5, 0)], "actorlayer")

game.camX = DisplayW / 2 - 16
game.camY = DisplayH / 2 - 16

newActor(Slime, 300, 200, None, "actorlayer")

# newActor(Slime, 500, 400, None, "actorlayer")

############### Testing ###############

############ Main game loop ##############


while running:
    clock.tick(FPS)

    for event in pg.event.get():
        keyboard.handle_event(event)
        if event.type == pg.QUIT:
            running = False

    window.fill(BLACK)
    game.GameMode()
    game.run()

    pg.display.update()
