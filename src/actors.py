import math

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

        runActors()

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

        game.camX = game.gmPlayer.shape.x - (DisplayW / 2) + game.gmPlayer.w / 2
        game.camY = game.gmPlayer.shape.y - (DisplayH / 2) + game.gmPlayer.h / 2

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
    game.camX = DisplayW / 2 + game.gmPlayer.w / 2
    game.camY = DisplayH / 2 + game.gmPlayer.h / 2
    game.GameMode = battleMode
    newActor(Soul, DisplayW / 2, DisplayH / 2, None, "actorlayer")
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
    # c.constructCircleAttack(game.gmPlayer.x, game.gmPlayer.y, 100, 60, 0, 200, (0, 0))


def battleMode():
    runActors()
    # print(game.camX)
    # print(game.camY)
    game.camX = 0
    game.camY = 0
    for i in game.attacks:
        i.run()
    # game.camX  = game.gmPlayer.shape.x - (DisplayW/2) + game.gmPlayer.w/2
    # game.camY = game.gmPlayer.shape.y - (DisplayH/2) + game.gmPlayer.h/2


def startPlay():
    pass


def saveGame():
    pass


def quitGame():
    pass


class gMap:
    def __init__(self, _map):
        self.mapdata = jsonRead(_map)

        # pg.image.load(self.mapdata["tilesets"][0]["image"]).convert()

    def drawTiles(self):
        # dataIterator = 0

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
                            # frame = game.loadSprite(tileset[0])
                            # Spawn different things depending on the layer?
                            if (
                                i["name"] == "BG"
                                or i["name"] == "FG"
                                or i["name"] == "MG"
                            ):
                                newActor(
                                    Sprite,
                                    x * 16,
                                    y * 16,
                                    [tileset[0], tileID - tileset[1]],
                                    i["name"],
                                )
                            if i["name"] == "solid":
                                newActor(
                                    Block,
                                    x * 16,
                                    y * 16,
                                    [tileID - tileset[1]],
                                    i["name"],
                                )
                                # print(tileset[1])
                            # drawSprite(tileset[0], frame[tileID - tileset[1]], x * 16 - game.camX, y * 16 - game.camY)
                        dataIterator += 1

            # if i["name"] == "solid": #Integrate this with the change made above
            #     for j in i["objects"]:
            #         newActor(Block, j["x"], j["y"] - 16, None, i["name"])

    def getTileset(self, tileGID):
        # print(tileGID)
        for i in range(0, len(self.mapdata["tilesets"])):
            tilesetGID = self.mapdata["tilesets"][i]["firstgid"]
            # print(i) #only prints 0, when it should print 1, 2 as well
            tilesetTileCount = self.mapdata["tilesets"][i]["tilecount"]
            if tileGID >= tilesetGID and tileGID < tilesetTileCount + tilesetGID:
                image = self.mapdata["tilesets"][i]["image"]
                # print(image)
                # print(i)
                # image.replace('..', 'res')
                return [pg.image.load(image.replace("..", "res")).convert(), tilesetGID]

        return [None, 0]


# p = gMap("res/map/test_for_PGE.json")


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

    def __init__(self, _x, _y, _arr=None):
        self.x = _x
        self.y = _y
        self.h = 16
        self.w = 16
        self.xspeed = 0
        self.yspeed = 0
        self.offsx = 0
        self.offsy = 0
        self.arr = _arr
        self.anim = None
        self.frame = None
        self.shape = None
        self.color = (100, 149, 237)
        self.frameIndex = 0
        self.id = Actor.id
        self.frame = []
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Are we sure pg.Rect takes height as the 3rd parameter and width as the 4th parameter?
        self.shape = pg.Rect(self.x, self.y, self.w, self.h)
        self.solid = False
        if self.arr != None:

            if len(self.arr) == 1:
                self.spriteSheet = self.arr[0]

    def loadSprite(self, _spr, _w=16, _h=16, _offs=(0, 0)):
        self.frame = []
        sprSize = _spr.get_size()
        sprW = int(sprSize[0])
        sprH = int(sprSize[1])

        if _offs == "centered":
            self.offsx = (_w - self.w) / 2
            self.offsy = (_h - self.h) / 2
        else:
            self.offsx = _offs[0]
            self.offsy = _offs[1]

        for i in range(0, int(sprH / _h)):
            for j in range(0, int(sprW / _w)):
                self.frame.append((j * _w, i * _h, _w, _h))

    def collision(self, _direction):
        for i in gmMap.actor:
            if i._typeof() == "Block":
                if i.shape.colliderect(self.shape):
                    if i.solid == True:
                        if _direction == "horizontal":
                            if self.xspeed > 0:
                                self.shape.right = i.shape.left

                            if self.xspeed < 0:
                                self.shape.left = i.shape.right

                        if _direction == "vertical":
                            if self.yspeed > 0:
                                self.shape.bottom = i.shape.top

                            if self.yspeed < 0:
                                self.shape.top = i.shape.bottom

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.camX,
                self.shape.y - game.camY,
                self.shape.w,
                self.shape.h,
            ),
        )

    def run(self):
        pass

    def render(self):
        pass
        # pg.draw.rect(window, (255, 255, 255), (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h))

    def destructor(self):
        pass

    def _typeof(self):
        return "Actor"


class Sprite(Actor):
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
        self.x = _x
        self.y = _y
        self.w = 16
        self.h = 16
        self.arr = _arr
        self.frame = []
        self.index = None
        if self.arr != None:

            if len(self.arr) >= 1:
                self.spriteSheet = self.arr[0]
                self.loadSprite(self.spriteSheet)
            if len(self.arr) >= 2:
                self.index = self.arr[1]

    def render(self):
        drawSprite(
            self.spriteSheet,
            self.frame[self.index],
            self.x - game.camX,
            self.y - game.camY,
        )
        # window.blit(self.spriteSheet, (self.x - game.camX, self.y - game.camY), self.frame[self.index])

    def _typeof(self):
        return "Sprite"


class Slime(Actor):
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
        self.x = _x
        self.y = _y
        self.w = 16
        self.h = 16
        self.arr = _arr
        self.frame = []
        self.anim = [0]
        self.timer = 0
        self.dist = 0
        self.jiggleAnim = [0, 3]
        self.direction = 0
        self.anim = self.jiggleAnim
        self.shape = pg.Rect(self.x, self.y, self.h, self.w)
        self.loadSprite(sprSlime, 32, 32, "centered")
        # print(self.frame)

    def debug(self):
        pg.draw.rect(
            window,
            RED,
            (
                self.shape.x - game.camX,
                self.shape.y - game.camY,
                self.shape.w,
                self.shape.h,
            ),
        )

    def get_distance_direction(self, _player):
        pass

    def run(self):
        self.frameIndex += 0.1
        self.dist = math.sqrt(
            (self.x - game.gmPlayer.x) ** 2 + (self.y - game.gmPlayer.y) ** 2
        )

        if game.gmPlayer.shape.colliderect(self.shape):
            startBattle()

        """if self.y-game.gmPlayer.y != 0:
            self.tangent = (self.x-game.gmPlayer.x)/(self.y-game.gmPlayer.y)

        if (self.x-game.gmPlayer.x)/(abs(self.x-game.gmPlayer.x)) != 0:
            self.xspeed = 0.5 * (self.x-game.gmPlayer.x)/(abs(self.x-game.gmPlayer.x))
        else:
            self.xspeed = 0
        
        if (self.y-game.gmPlayer.y)/(abs(self.y-game.gmPlayer.y)) != 0:
            self.yspeed = 0.5 * self.tangent * (self.y-game.gmPlayer.y)/(abs(self.y-game.gmPlayer.y))
        else:
            self.yspeed = 0"""

        self.x += self.xspeed
        self.y += self.yspeed
        if self.dist < 50:
            pass
            # print("dist")

    def render(self):
        # pass
        drawSprite(
            sprSlime,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))
            ],
            self.x - game.camX - self.offsx,
            self.y - game.camY - self.offsy,
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


"""def runActors():
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

    """for i in gmMap.actor:
        if i._typeof() == "Sprite":
            i.render()
            if game.debugMode == True:
                i.debug()

    for i in gmMap.actor:
        if i._typeof() == "Block":
            i.render()
            if game.debugMode == True:
                i.debug()
    
    for i in gmMap.actor:
        if i._typeof() == "Tux":
            i.render()
            if game.debugMode == True:
                i.debug()
    
    for i in gmMap.actor:
        if i._typeof() == "Slime":
            i.render()
            if game.debugMode == True:
                i.debug()"""


"""def newActor(_type, _x, _y, _arr = None, _layer = "None"):
    na = _type(_x, _y, _arr)
    na.id = gmMap.actlast
    game.actor[_layer].append(na)
    gmMap.actlast += 1"""


class VerticallyMovingBlock(Actor):
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
        self.originalY = _y
        self.loadSprite(sprBlock)
        self.solid = True
        self.color = (200, 200, 200)
        self.frameCount = 0
        if not self.arr:
            return
        if self.arr.len() == 1:
            self.spriteSheet = self.arr[0]
            self.loadSprite(self.spriteSheet)

    def run(self):
        self.frameCount += 1

        self.y = self.originalY + math.sin(self.frameCount / 25) * 32

        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        drawSprite(sprBlock, self.frame[0], self.x - game.camX, self.y - game.camY)
        # pg.draw.rect(window, self.color, (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h), 0)

    def _typeof(self):
        return "Block"

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.camX,
                self.shape.y - game.camY,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )


class HorizontallyMovingBlock(Actor):
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
        self.originalX = _x
        self.x = _x
        self.y = _y
        self.w = 16
        self.h = 16
        self.arr = _arr
        self.shape = pg.Rect(self.x, self.y, self.h, self.w)
        self.loadSprite(sprBlock)
        self.solid = True
        self.color = (200, 200, 200)
        self.frameCount = 0
        if not self.arr:
            return
        if self.arr.len() == 1:
            self.spriteSheet = self.arr[0]
            self.loadSprite(self.spriteSheet)

    def run(self):
        self.frameCount += 1

        self.x = self.originalX + math.sin(self.frameCount / 25) * 32

        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        drawSprite(sprBlock, self.frame[0], self.x - game.camX, self.y - game.camY)
        # pg.draw.rect(window, self.color, (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h), 0)

    def _typeof(self):
        return "Block"

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.camX,
                self.shape.y - game.camY,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )


class Block(Actor):
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
        self.solidOffsx = 0
        self.solidOffsy = 0
        self.shape = pg.Rect(self.x, self.y, self.w, self.h)
        # self.loadSprite(sprBlock)
        self.solid = True
        self.color = (100, 100, 100)
        self.anim = [0.0, 0.0]
        self.solid = True
        self.sort = 0
        self.spriteSheet = sprBlock
        if self.arr != None:

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
                # self.spriteSheet = self.arr[0]
                # self.loadSprite(self.arr[0])
            if len(self.arr) >= 2:
                self.sort = self.arr[1]
            if len(self.arr) >= 3:
                self.solid = self.arr[2]
                if self.solid == False:
                    self.color = (200, 200, 200, 90)

    def run(self):
        self.shape.x = self.x + self.solidOffsx
        self.shape.y = self.y + self.solidOffsy
        self.frameIndex += 0.14
        # print(self.spriteSheet)

    def render(self):
        pass
        # if self.arr:
        # drawSprite(self.spriteSheet, self.frame[int(self.anim[0]) + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))], self.x - game.camX, self.y - game.camY)
        # pg.draw.rect(window, self.color, (self.shape.x -  game.camX, self.shape.y - game.camY, self.shape.w, self.shape.h), 0)

    def _typeof(self):
        return "Block"

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.camX,
                self.shape.y - game.camY,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )


class Tux(Actor):
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
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
        self.loadSprite(sprTux)
        self.solid = False
        self.color = (0, 255, 0)
        game.gmPlayer = self
        print(game.gmPlayer)
        if not _arr:
            return

    def run(self):

        if not keyboard.is_held(RIGHT) or not keyboard.is_held(LEFT):
            self.xspeed = 0

        if not keyboard.is_held(UP) or not keyboard.is_held(DOWN):
            self.yspeed = 0

        if keyboard.is_held(RIGHT):
            self.xspeed = 1
            self.anim = self.walkRight
            self.standStillAnim = self.standRight

        if keyboard.is_held(LEFT):
            self.xspeed = -1
            self.anim = self.walkLeft
            self.standStillAnim = self.standLeft

        if keyboard.is_held(UP):
            self.yspeed = -1
            self.anim = self.walkUp
            self.standStillAnim = self.standUp

        if keyboard.is_held(DOWN):
            self.yspeed = 1
            self.anim = self.walkDown
            self.standStillAnim = self.standDown

        if (
            keyboard.is_pressed(RIGHT)
            or keyboard.is_pressed(LEFT)
            or keyboard.is_pressed(UP)
            or keyboard.is_pressed(DOWN)
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
            sprTux,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))
            ],
            self.shape.x - game.camX,
            self.shape.y - game.camY,
        )

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.camX,
                self.shape.y - game.camY,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )

    def _typeof(self):
        return "Tux"


class Soul(Actor):
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
        self.x = _x
        self.y = _y
        self.w = 8
        self.h = 8
        self.arr = _arr
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
        self.loadSprite(sprSoul, 8, 8)
        print(self.frame)
        self.solid = False
        self.color = (0, 255, 0)
        game.gmPlayer = self
        print(game.gmPlayer)
        if not _arr:
            return

    def run(self):

        if not get_control("right", "held") or not get_control("left", "held"):
            self.xspeed = 0

        if not get_control("up", "held") or not get_control("down", "held"):
            self.yspeed = 0

        if get_control("right", "held"):
            self.xspeed = 1

        if get_control("left", "held"):
            self.xspeed = -1

        if get_control("up", "held"):
            self.yspeed = -1

        if get_control("down", "held"):
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
            sprSoul,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))
            ],
            self.shape.x - game.camX,
            self.shape.y - game.camY,
        )

    def debug(self):
        pg.draw.rect(
            window,
            self.color,
            (
                self.shape.x - game.camX,
                self.shape.y - game.camY,
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
        self.loadSprite(sprBullet, 4, 4)
        if self.arr != None:
            self.xspeed = self.arr[0][0]
            self.yspeed = self.arr[0][1]
        # print(self.frame)

    def debug(self):
        pg.draw.rect(
            window,
            RED,
            (
                self.shape.x - game.camX,
                self.shape.y - game.camY,
                self.shape.w,
                self.shape.h,
            ),
        )

    def run(self):
        self.frameIndex += 0.1

        if game.gmPlayer.shape.colliderect(self.shape):
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
            sprBullet,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frameIndex % (self.anim[-1] - self.anim[0] + 1))
            ],
            self.x - game.camX,
            self.y - game.camY,
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
                    newActor(object, x, y, arr, "actorlayer")

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
