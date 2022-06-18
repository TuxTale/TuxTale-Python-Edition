import math
from itertools import cycle



from .controls import *
from .init import *


def gmPlay():
    if game:
        # 1) UPDATE PHASE
        #
        # Create, update, and destroy actors
        #   For instance, new actors may be created (maybe spawned by something else or some event)
        #   Each actor must update its current state based on what's going on
        #   Some actors might "die" (be killed or despawn) and be removed from the game

        run_actors()

        # 2) CAMERA PHASE
        #
        # Determine where the camera is. The camera phase occurs after the update phase, because
        # we want all actors to have finished processing (and figured out their new x-, y- positions,
        # and what they're doing) before we decide where to place the camera.
        #
        # Currently, the camera just follows Tux around, but we could imagine more
        # complicated scenarios.
        #
        # For instance, if Tux is on the edge of the map, the camera may stop scrolling.
        # Cut scenes, boss introductions, or special triggers may require customized control
        # of the camera.
        # Visual effects such as screen-shake may also cause the camera's position to change.

        game.cam_x = game.gm_player.shape.x - (DisplayW / 2) + game.gm_player.w / 2
        game.cam_y = game.gm_player.shape.y - (DisplayH / 2) + game.gm_player.h / 2

        # 3) RENDER PHASE
        #
        # Render each actor and whatever else (e.g. particle effects, etc) needs to be rendered.
        # The render phase happens after both the update and camera phase. This ensures that literally
        # nothing is drawn to the screen until after we've finalized the location of the camera.
        # (This is in contrast to a mixed update-and-render approach. In such an approach, it would be
        # difficult for any actor to change the location of the camera during their run() processing,
        # since other actors may have already rendered themselves onto the screen, if such actors had
        # their run() method processed first.)
        #
        # It may be necessary to order the actors by z-index during a render phase if actors
        # can overlap each other.
        # For instance, if a large sprite shoots small bullets, the bullets should probably be rendered
        # on top of (rather than behind) the large sprite. This means that the bullets must be rendered
        # after the large sprite.
        # (Note that the order in which objects are rendered does not necessarily need to be the same order
        # in which we invoke the run() method.)

        # renderActors()


def startBattle():
    game.unusedActors = game.actor
    game.actor = {
        "solid": [],
        "BG": [],
        "MG": [],
        "actorlayer": [],
        "FG": [],
        "attacks": [],
    }
    game.cam_x = DisplayW / 2 + game.gm_player.w / 2
    game.cam_y = DisplayH / 2 + game.gm_player.h / 2
    game.game_mode = battleMode
    new_actor(Soul, DisplayW / 2, DisplayH / 2, None, "actorlayer")
    c = Attack(Slime)
    game.attacks.append(c)
    c.constructAttack(0, 100, 0, 20, 60, 10, 10, (2, -0.5))
    c.constructAttack(400, 100, 0, 20, 60, 10, 10, (-2, -0.5))
    c.constructAttack(0, 100, 0, 20, 120, 10, 10, (2, -0.5))
    c.constructAttack(400, 100, 0, 20, 120, 10, 10, (-2, -0.5))
    c.constructAttack(0, 100, 0, 20, 180, 10, 10, (2, -0.5))
    c.constructAttack(400, 100, 0, 20, 180, 10, 10, (-2, -0.5))
    """for i in range(0, 50):
        c.constructAttack(math.sin(i*10), 100, 0, 20, 180, 10, 10, (math.sin(i), -math.sin(i)))"""
    # c.constructCircleAttack(game.gm_player.x, game.gm_player.y, 100, 60, 0, 200, (0, 0))


def battleMode():
    run_actors()
    # print(game.cam_x)
    # print(game.cam_y)
    game.cam_x = 0
    game.cam_y = 0
    for i in game.attacks:
        i.run()
    # game.cam_x  = game.gm_player.shape.x - (DisplayW/2) + game.gm_player.w/2
    # game.cam_y = game.gm_player.shape.y - (DisplayH/2) + game.gm_player.h/2


def startPlay():
    pass


def saveGame():
    pass


def quitGame():
    pass


class gMap:
    def __init__(self, _map):
        self.mapdata = json_read(_map)

    def draw_tiles(self):
        for i in self.mapdata["layers"]:
            # print(i["name"])
            game.actor[i["name"]] = []
            if i["type"] == "tilelayer":
                dataIterator = 0
                for y in range(0, i["height"]):
                    for x in range(0, i["width"]):
                        tileID = i["data"][dataIterator]
                        # print(dataIterator)
                        if tileID > 0:
                            tileset = self.getTileset(tileID)
                            # frame = game.load_sprite(tileset[0])
                            # Spawn different things depending on the layer?
                            if (
                                    i["name"] == "BG"
                                    or i["name"] == "FG"
                                    or i["name"] == "MG"
                            ):
                                new_actor(
                                    Sprite,
                                    x * 16,
                                    y * 16,
                                    [tileset[0], tileID - tileset[1]],
                                    i["name"],
                                )
                            if i["name"] == "solid":
                                new_actor(
                                    Block,
                                    x * 16,
                                    y * 16,
                                    [tileID - tileset[1]],
                                    i["name"],
                                )
                                # print(tileset[1])
                            # drawSprite(tileset[0], frame[tileID - tileset[1]], x * 16 - game.cam_x, y * 16 - game.cam_y)
                        dataIterator += 1

            # if i["name"] == "solid": #Integrate this with the change made above
            #     for j in i["objects"]:
            #         new_actor(Block, j["x"], j["y"] - 16, None, i["name"])

    def getTileset(self, tileGID):

        for i in range(0, len(self.mapdata["tilesets"])):
            tilesetGID = self.mapdata["tilesets"][i]["firstgid"]
            # print(i) #only prints 0, when it should print 1, 2 as well
            tilesetTileCount = self.mapdata["tilesets"][i]["tilecount"]
            if tilesetGID <= tileGID < tilesetTileCount + tilesetGID:
                image = self.mapdata["tilesets"][i]["image"]
                return [pg.image.load(image.replace("..", "res")).convert(), tilesetGID]

        return [None, 0]


class Physactor:
    def __init__(self, _x, _y):
        self.x = _x
        self.y = _y
        self.w = 0
        self.h = 0
        self.xprev = _x
        self.yprev = _y

    def run(self):
        pass

    def render(self):
        pass


class Actor:
    id = 0

    def __init__(self, x, y, arr=None):
        self.x = x
        self.y = y
        self.h = 16
        self.w = 16
        self.xspeed = 0
        self.yspeed = 0
        self.offsx = 0
        self.offsy = 0
        self.arr = arr
        self.anim = None
        self.frame = None
        self.shape = None
        self.color = (100, 149, 237)
        self.frameIndex = 0
        self.id = Actor.id
        self.frame = []
        self.shape = pg.Rect(self.x, self.y, self.w, self.h)
        self.solid = False
        if self.arr is not None:
            if len(self.arr) == 1:
                self.sprite_sheet = self.arr[0]

    def load_sprite(self, spr, w=16, h=16, offs=(0, 0)):
        self.frame = []
        sprite_size = spr.get_size()
        sprite_w = int(sprite_size[0])
        sprite_h = int(sprite_size[1])

        if offs == "centered":
            self.offsx = (w - self.w) / 2
            self.offsy = (h - self.h) / 2
        else:
            self.offsx = offs[0]
            self.offsy = offs[1]

        for i in range(0, int(sprite_h / h)):
            for j in range(0, int(sprite_w / w)):
                self.frame.append((j * w, i * h, w, h))

    def collision(self, direction):
        for i in gmMap.actor:
            if i._typeof() == "Block":
                if i.shape.colliderect(self.shape):
                    if i.solid == True:
                        if direction == "horizontal":
                            if self.xspeed > 0:
                                self.shape.right = i.shape.left

                            if self.xspeed < 0:
                                self.shape.left = i.shape.right

                        if direction == "vertical":
                            if self.yspeed > 0:
                                self.shape.bottom = i.shape.top

                            if self.yspeed < 0:
                                self.shape.top = i.shape.bottom

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
        )

    def run(self):
        pass

    def render(self):
        pass

    def destructor(self):
        pass

    def _typeof(self):
        return "Actor"


class Sprite(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr=None)
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.arr = arr
        self.frame = []
        self.index = None
        if self.arr is not None:
            if len(self.arr) >= 1:
                self.sprite_sheet = self.arr[0]
                self.load_sprite(self.sprite_sheet)
            if len(self.arr) >= 2:
                self.index = self.arr[1]

    def render(self):
        drawSprite(
            self.sprite_sheet,
            self.frame[self.index],
            self.x - game.cam_x,
            self.y - game.cam_y,
        )

    def _typeof(self):
        return "Sprite"


class Slime(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.arr = arr
        self.frame = []
        self.anim = [0]
        self.timer = 0
        self.dist = 0
        self.jiggleAnim = [0, 3]
        self.direction = 0
        self.anim = self.jiggleAnim
        self.shape = pg.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_slime, 32, 32, "centered")
        # print(self.frame)

    def debug(self):
        pg.draw.rect(
            window,
            RED,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
        )

    def run(self):
        if game.gm_player.shape.colliderect(self.shape):
            startBattle()

        direction = (pg.math.Vector2(game.gm_player.shape.topleft) - pg.math.Vector2(self.shape.topleft)).normalize()
        self.x += direction.x * 0.5
        self.y += direction.y * 0.5
        self.shape.topleft = self.x, self.y

        self.frameIndex += 0.1

    def render(self):
        # pass
        drawSprite(
            sprite_slime,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))
                ],
            self.x - game.cam_x - self.offsx,
            self.y - game.cam_y - self.offsy,
        )

    def _typeof(self):
        return "Slime"


def collisionCheck(rectangle):
    for i in game.actor["solid"]:

        if i.shape.colliderect(rectangle):
            if i.solid == True:
                # If a collision happens, we can resolve the collision by moving in one of
                # 4 possible directions (and moving until there is no longer any overlap).
                # The desired direction we want to go is whichever one requires us to move
                # the fewest number of pixels.

                # amount of pixels we need to move leftward to avoid overlap
                distanceToLeft = rectangle.right - i.shape.left

                # amount of pixels we need to move rightward to avoid overlap
                distanceToRight = i.shape.right - rectangle.left

                if distanceToLeft < distanceToRight:
                    distanceToMoveX = -distanceToLeft
                else:
                    distanceToMoveX = distanceToRight

                distanceToTop = rectangle.bottom - i.shape.top

                distanceToBottom = i.shape.bottom - rectangle.top

                if distanceToTop < distanceToBottom:
                    distanceToMoveY = -distanceToTop
                else:
                    distanceToMoveY = distanceToBottom

                if abs(distanceToMoveX) < abs(distanceToMoveY):
                    return {
                        "hasCollided": True,
                        "newRectangle": pg.Rect(
                            rectangle.x + distanceToMoveX,
                            rectangle.y,
                            rectangle.w,
                            rectangle.h,
                        ),
                    }
                if abs(distanceToMoveX) > abs(distanceToMoveY):
                    return {
                        "hasCollided": True,
                        "newRectangle": pg.Rect(
                            rectangle.x,
                            rectangle.y + distanceToMoveY,
                            rectangle.w,
                            rectangle.h,
                        ),
                    }
                if abs(distanceToMoveX) > abs(distanceToMoveY):
                    return {
                        "hasCollided": True,
                        "newRectangle": pg.Rect(
                            rectangle.x + distanceToMoveX,
                            rectangle.y + distanceToMoveY,
                            rectangle.w,
                            rectangle.h,
                        ),
                    }

    return {"hasCollided": False}


"""def run_actors():
    for i in game.actor.values():
        for j in i:
            j.render()
            if game.debugMode == True:
                j.debug()
            j.run()
            #j.render()"""


def renderActors():
    for i in game.actor.values():
        for j in i:
            j.render()

class VerticallyMovingBlock(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.originalY = y
        self.load_sprite(sprite_block)
        self.solid = True
        self.color = (200, 200, 200)
        self.frameCount = 0
        if not self.arr:
            return
        if self.arr.len() == 1:
            self.sprite_sheet = self.arr[0]
            self.load_sprite(self.sprite_sheet)

    def run(self):
        self.frameCount += 1

        self.y = self.originalY + math.sin(self.frameCount / 25) * 32

        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        drawSprite(sprite_block, self.frame[0], self.x - game.cam_x, self.y - game.cam_y)

    def _typeof(self):
        return "Block"

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )


class HorizontallyMovingBlock(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.originalX = x
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.arr = arr
        self.shape = pg.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_block)
        self.solid = True
        self.color = (200, 200, 200)
        self.frameCount = 0
        if not self.arr:
            return
        if self.arr.len() == 1:
            self.sprite_sheet = self.arr[0]
            self.load_sprite(self.sprite_sheet)

    def run(self):
        self.frameCount += 1

        self.x = self.originalX + math.sin(self.frameCount / 25) * 32

        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        drawSprite(sprite_block, self.frame[0], self.x - game.cam_x, self.y - game.cam_y)

    def _typeof(self):
        return "Block"

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )


class Block(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.solidOffsx = 0
        self.solidOffsy = 0
        self.shape = pg.Rect(self.x, self.y, self.w, self.h)
        # self.load_sprite(sprite_block)
        self.solid = True
        self.color = (100, 100, 100)
        self.anim = [0.0, 0.0]
        self.solid = True
        self.sort = 0
        self.sprite_sheet = sprite_block
        if self.arr is not None:
            if len(self.arr) >= 1:
                self.sort = self.arr[0]
                if self.sort == 0:
                    self.shape.w = 16
                    self.shape.h = 16
                if self.sort == 1:
                    self.shape.w = 16
                    self.shape.h = 8
                if self.sort == 2:
                    self.solidOffsx = 0
                    self.solidOffsy = 8
                    self.shape.w = 16
                    self.shape.h = 8
                if self.sort == 3:
                    self.solidOffsx = 0
                    self.solidOffsy = 0
                    self.shape.w = 8
                    self.shape.h = 16
                if self.sort == 4:
                    self.solidOffsx = 8
                    self.solidOffsy = 0
                    self.shape.w = 8
                    self.shape.h = 16

            if len(self.arr) >= 2:
                self.sort = self.arr[1]
            if len(self.arr) >= 3:
                self.solid = self.arr[2]
                if not self.solid:
                    self.color = (200, 200, 200, 90)

    def run(self):
        self.shape.x = self.x + self.solidOffsx
        self.shape.y = self.y + self.solidOffsy
        self.frameIndex += 0.14

    def render(self):
        pass
        # if self.arr:
        # drawSprite(self.sprite_sheet, self.frame[int(self.anim[0]) + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))], self.x - game.cam_x, self.y - game.cam_y)
        # pg.draw.rect(window, self.color, (self.shape.x -  game.cam_x, self.shape.y - game.cam_y, self.shape.w, self.shape.h), 0)

    def _typeof(self):
        return "Block"

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )


class Tux(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.frame = []
        self.walkRight = [0.0, 3.0]
        self.walkUp = [4.0, 7.0]
        self.walkDown = [8.0, 11.0]
        self.walkLeft = [12.0, 15.0]
        self.standRight = [0]
        self.standLeft = [12]
        self.standUp = [4]
        self.standDown = [8]
        self.anim = self.walkRight
        self.standStillAnim = self.standRight
        self.xspeed = 0
        self.yspeed = 0
        self.autocon = False
        self.idle = False
        self.stepCount = 0
        self.shape = pg.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_tux)
        self.solid = False
        self.color = (0, 255, 0)
        game.gm_player = self
        print(game.gm_player)
        if not arr:
            return

    def run(self):

        if not getcon("right", "held") or not getcon("left", "held"):
            self.xspeed = 0

        if not getcon("up", "held") or not getcon("down", "held"):
            self.yspeed = 0

        if getcon("right", "held"):
            self.xspeed = 1
            self.anim = self.walkRight
            self.standStillAnim = self.standRight

        if getcon("left", "held"):
            self.xspeed = -1
            self.anim = self.walkLeft
            self.standStillAnim = self.standLeft

        if getcon("up", "held"):
            self.yspeed = -1
            self.anim = self.walkUp
            self.standStillAnim = self.standUp

        if getcon("down", "held"):
            self.yspeed = 1
            self.anim = self.walkDown
            self.standStillAnim = self.standDown

        if (
                getcon("right", "press")
                or getcon("left", "press")
                or getcon("up", "press")
                or getcon("down", "press")
        ):
            self.stepCount += 1
            if self.stepCount % 2 == 0:
                self.frameIndex = 1
            else:
                self.frameIndex = 3

        # hasSuccessfullyMoved is true only if Tux managed to move in a desired direction
        # without bumping into a wall.
        #
        # So if a vertical wall is to the immediate right of Tux, and Tux is moving rightward,
        # Tux hasn't successfully moved.
        #
        # In contrast, if Tux is moving both up and to the right, then Tux has successfully moved
        # even though the wall is impeding Tux's rightward movement (since Tux is still moving upward).
        hasSuccessfullyMoved = False

        # Attempt to move in the x-axis by xspeed (note xspeed may be 0)
        collisionCheckResult = collisionCheck(
            pg.Rect(
                self.shape.x + self.xspeed, self.shape.y, self.shape.w, self.shape.h
            )
        )
        if collisionCheckResult["hasCollided"]:
            self.shape = collisionCheckResult["newRectangle"]
        else:
            self.shape.x += self.xspeed
            self.x += self.xspeed
            hasSuccessfullyMoved = hasSuccessfullyMoved or (self.xspeed != 0)

        # Attempt to move in the y-axis by yspeed
        collisionCheckResult = collisionCheck(
            pg.Rect(
                self.shape.x, self.shape.y + self.yspeed, self.shape.w, self.shape.h
            )
        )
        if collisionCheckResult["hasCollided"]:
            self.shape = collisionCheckResult["newRectangle"]
        else:
            self.shape.y += self.yspeed
            self.y += self.yspeed
            hasSuccessfullyMoved = hasSuccessfullyMoved or (self.yspeed != 0)

        if not hasSuccessfullyMoved or (self.xspeed == 0 and self.yspeed == 0):
            self.anim = self.standStillAnim

        self.frameIndex += 0.14

    def render(self):
        drawSprite(
            sprite_tux,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))
                ],
            self.shape.x - game.cam_x,
            self.shape.y - game.cam_y,
        )

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )

    def _typeof(self):
        return "Tux"


class Soul(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8
        self.arr = arr
        self.frame = []
        self.visible = [0]
        self.invisible = [0, 1]
        self.anim = self.visible
        self.xspeed = 0
        self.yspeed = 0
        self.autocon = False
        self.idle = False
        self.stepCount = 0
        self.shape = pg.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_soul, 8, 8)
        print(self.frame)
        self.solid = False
        self.color = (0, 255, 0)
        game.gm_player = self
        print(game.gm_player)
        if not arr:
            return

    def run(self):

        if not getcon("right", "held") or not getcon("left", "held"):
            self.xspeed = 0

        if not getcon("up", "held") or not getcon("down", "held"):
            self.yspeed = 0

        if getcon("right", "held"):
            self.xspeed = 1

        if getcon("left", "held"):
            self.xspeed = -1

        if getcon("up", "held"):
            self.yspeed = -1

        if getcon("down", "held"):
            self.yspeed = 1

        # hasSuccessfullyMoved is true only if Tux managed to move in a desired direction
        # without bumping into a wall.
        #
        # So if a vertical wall is to the immediate right of Tux, and Tux is moving rightward,
        # Tux hasn't successfully moved.
        #
        # In contrast, if Tux is moving both up and to the right, then Tux has successfully moved
        # even though the wall is impeding Tux's rightward movement (since Tux is still moving upward).
        hasSuccessfullyMoved = False

        # Attempt to move in the x-axis by xspeed (note xspeed may be 0)
        collisionCheckResult = collisionCheck(
            pg.Rect(
                self.shape.x + self.xspeed, self.shape.y, self.shape.w, self.shape.h
            )
        )
        if collisionCheckResult["hasCollided"]:
            self.shape = collisionCheckResult["newRectangle"]
        else:
            self.shape.x += self.xspeed
            self.x += self.xspeed
            hasSuccessfullyMoved = hasSuccessfullyMoved or (self.xspeed != 0)

        # Attempt to move in the y-axis by yspeed
        collisionCheckResult = collisionCheck(
            pg.Rect(
                self.shape.x, self.shape.y + self.yspeed, self.shape.w, self.shape.h
            )
        )
        if collisionCheckResult["hasCollided"]:
            self.shape = collisionCheckResult["newRectangle"]
        else:
            self.shape.y += self.yspeed
            self.y += self.yspeed
            hasSuccessfullyMoved = hasSuccessfullyMoved or (self.yspeed != 0)

        if not hasSuccessfullyMoved or (self.xspeed == 0 and self.yspeed == 0):
            pass
            # self.anim = self.standStillAnim

        if game.hurtTimer > 0:
            self.anim = self.invisible
        else:
            self.anim = self.visible

        self.frameIndex += 0.14

    def render(self):
        drawSprite(
            sprite_soul,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))
                ],
            self.shape.x - game.cam_x,
            self.shape.y - game.cam_y,
        )

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )

    def _typeof(self):
        return "Soul"


class Bullet(Actor):
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
        self.x = _x
        self.y = _y
        self.w = 4
        self.h = 4
        self.arr = _arr
        self.frame = []
        self.anim = [0]
        self.xspeed = 0
        self.yspeed = 0
        self.timer = 0
        self.dist = 0
        self.direction = 0
        self.shape = pg.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_bullet, 4, 4)
        if self.arr != None:
            self.xspeed = self.arr[0][0]
            self.yspeed = self.arr[0][1]
        # print(self.frame)

    def debug(self):
        pg.draw.rect(
            window,
            RED,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
        )

    def run(self):
        self.frameIndex += 0.1

        if game.gm_player.shape.colliderect(self.shape):
            # print("hurt")
            if game.hurtTimer == 0:
                game.health -= 1
                game.hurtTimer = 60
                print(game.health)
        # print(self.xspeed)
        self.x += self.xspeed
        self.y += self.yspeed
        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        # pass
        drawSprite(
            sprite_bullet,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))
                ],
            self.x - game.cam_x,
            self.y - game.cam_y,
        )

    def _typeof(self):
        return "Bullet"


animation = {"events": []}


class Attack:
    def __init__(self, _opponent, _timer=0):
        self.opponent = _opponent
        self.timer = 0

    def run(self):
        self.timer += 1
        for i in animation["events"]:
            if self.timer >= i["start"] and self.timer < i["stop"]:
                spawn = i["spawn"]
                for j in range(0, len(spawn)):
                    entity = spawn[j]["entity"]
                    object = entity["object"]
                    x = entity["x"]
                    y = entity["y"]
                    arr = entity["arr"]
                    new_actor(object, x, y, arr, "actorlayer")

    def constructAttack(self, _x, _y, _xspace, _yspace, _start, _wait, _number, _speed):

        for i in range(0, _number):
            dict = {
                "start": _start + i * _wait,
                "stop": _start + i * _wait + 1,
                "function": 0,
                "spawn": [
                    {
                        "entity": {
                            "object": Bullet,
                            "x": _x + _xspace * i,
                            "y": _y + _yspace * i,
                            "arr": [(_speed[0], _speed[1])],
                        },
                    }
                ],
            }

            animation["events"].append(dict)

    def constructCircleAttack(self, _x, _y, _r, _start, _wait, _number, _speed):
        for i in range(0, _number):
            dv = 2 * math.pi / _number
            dict = {
                "start": _start + i * _wait,
                "stop": _start + i * _wait + 1,
                "function": 0,
                "spawn": [
                    {
                        "entity": {
                            "object": Bullet,
                            "x": _x + math.cos(dv * i) * _r,
                            "y": _y + math.sin(dv * i) * _r,
                            "arr": [(_speed[0], _speed[1])],
                        },
                    }
                ],
            }

            animation["events"].append(dict)
