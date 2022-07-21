from cgitb import text
from .controls import *
from .utils import *
from .init import *
import math
from .textboxes import TextBox, Dialogue

def game_play():
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

        game.cam_x = game.game_player.shape.center[0] - (display_w / 2)
        game.cam_y = game.game_player.shape.center[1] - (display_H / 2)

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
        # render_actors()


def start_battle():
    game.unused_actors = game.actor

    game.actor = {
        "solid": [],
        "BG": [],
        "MG": [],
        "actorlayer": [],
        "FG": [],
        "attacks": [],
    }

    game.cam_x = display_w / 2 + game.game_player.w / 2
    game.cam_y = display_H / 2 + game.game_player.h / 2
    game.game_mode = battle_mode

    new_actor(Soul, display_w / 2, display_H / 2, None, "actorlayer")
    c = Attack(Slime)
    game.attacks.append(c)
    
    c.construct_attack(0, 100, 0, 20, 60, 10, 10, (2, -0.5))
    c.construct_attack(400, 100, 0, 20, 60, 10, 10, (-2, -0.5))
    c.construct_attack(0, 100, 0, 20, 120, 10, 10, (2, -0.5))
    c.construct_attack(400, 100, 0, 20, 120, 10, 10, (-2, -0.5))
    c.construct_attack(0, 100, 0, 20, 180, 10, 10, (2, -0.5))
    c.construct_attack(400, 100, 0, 20, 180, 10, 10, (-2, -0.5))


def battle_mode():
    run_actors()

    game.cam_x = 0
    game.cam_y = 0
    
    for i in game.attacks:
        i.run()


def start_play():
    pass


def save_game():
    pass


def quit_game():
    pass


class GameMap:
    def __init__(self, _map):
        self.mapdata = json_read(_map)

    def draw_tiles(self):
        for i in self.mapdata["layers"]:
            game.actor[i["name"]] = []
                            
            if i["type"] == "tilelayer":
                data_iterator = 0
                for y in range(0, i["height"]):
                    for x in range(0, i["width"]):
                        tile_id = i["data"][data_iterator]

                        if tile_id > 0:
                            tileset = self.get_tileset(tile_id)

                            if i["name"] == "BG" or i["name"] == "FG" or i["name"] == "MG":
                                new_actor(
                                    Sprite,
                                    x * 16,
                                    y * 16,
                                    [tileset[0], tile_id - tileset[1], (tileset[2], tileset[3])],
                                    i["name"],
                                )
                            
                            if i["name"] == "solid":
                                new_actor(
                                    Block,
                                    x * 16,
                                    y * 16,
                                    [tile_id - tileset[1], tileset[0], tile_id - tileset[1]],
                                    i["name"],
                                )
                        data_iterator += 1
            if i["type"] == "objectgroup":
                for j in i["objects"]: 
                    n = j["gid"] - self.get_actorsheet()[1]
                    if n == 0:
                        new_actor(Tux, j["x"], j["y"], None, i["name"])
                    if n == 1:
                        new_actor(Slime, j["x"], j["y"], None, i["name"])

    def get_tileset(self, tile_GID):
        for i in range(0, len(self.mapdata["tilesets"])):
            tileset_GID = self.mapdata["tilesets"][i]["firstgid"]
            tileset_tile_count = self.mapdata["tilesets"][i]["tilecount"]

            if tileset_GID <= tile_GID < tileset_tile_count + tileset_GID:
                image = self.mapdata["tilesets"][i]["image"]
                tilewidth = self.mapdata["tilesets"][i]["tilewidth"]
                tileheight = self.mapdata["tilesets"][i]["tileheight"]
                return [pygame.image.load(image.replace("..", "res")).convert_alpha(), tileset_GID, tilewidth, tileheight]
        
        return [None, 0]
    
    def get_actorsheet(self):
        for i in self.mapdata["tilesets"]:
            if i["name"] == "actorsheet":
                return (i["image"], i["firstgid"])

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
        self.frame_index = 0
        self.id = Actor.id
        self.frame = []

        # Are we sure pygame.Rect takes height as the 3rd parameter and width as the 4th parameter?
        
        self.shape = pygame.Rect(self.x, self.y, self.w, self.h)
        self.solid = False

        if self.arr != None:
            if len(self.arr) == 1:
                self.sprite_sheet = self.arr[0]

    def load_sprite(self, _spr, _w=16, _h=16, _offs=(0, 0)):
        self.frame = []
        sprite_size = _spr.get_size()
        sprite_w = int(sprite_size[0])
        sprite_h = int(sprite_size[1])

        if _offs == "centered":
            self.offsx = (_w - self.w) / 2
            self.offsy = (_h - self.h) / 2
        else:
            self.offsx = _offs[0]
            self.offsy = _offs[1]

        for i in range(0, int(sprite_h / _h)):
            for j in range(0, int(sprite_w / _w)):
                self.frame.append((j * _w, i * _h, _w, _h))

    def collision(self, _direction):
        for i in game_map.actor:
            if i.typeof() == "Block":
                if i.shape.colliderect(self.shape):
                    if i.solid:
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
        pass

    def run(self):
        pass

    def render(self):
        pass

    def destructor(self):
        pass

    def typeof(self):
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

        if self.arr is not None:
            if len(self.arr) >= 1:
                self.sprite_sheet = self.arr[0]
                self.load_sprite(self.sprite_sheet)
            
            if len(self.arr) >= 2:
                self.index = self.arr[1]
            
            if len(self.arr) >= 3:
                self.size = self.arr[2]
                self.load_sprite(self.sprite_sheet, self.size[0], self.size[1])

    def render(self):
        draw_sprite(
            self.sprite_sheet,
            self.frame[self.index],
            self.x - game.cam_x,
            self.y - game.cam_y,
        )

    def typeof(self):
        return "Sprite"


def collision_check(rectangle):
    return any(i.shape.colliderect(rectangle) and i.solid for i in game.actor["solid"])


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
        self.shape = pygame.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_slime, 32, 32, "centered")

    def debug(self):
        pygame.draw.rect(
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
        if game.game_player.shape.colliderect(self.shape):
            start_battle()

        self.xspeed, self.yspeed = ((
                    pygame.math.Vector2(game.game_player.shape.topleft) - pygame.math.Vector2(self.shape.topleft)
        ).normalize() * 0.5).xy

        # Attempt to move in the x-axis by xspeed

        if collision_check(pygame.Rect(self.shape.x + self.xspeed, self.shape.y, self.shape.w, self.shape.h)):
            self.xspeed = 0
        else:
            self.x += self.xspeed
            self.shape.topleft = self.x, self.y
        
        # Attempt to move in the y-axis by yspeed

        if collision_check(pygame.Rect(self.shape.x, self.shape.y + self.yspeed, self.shape.w, self.shape.h)):
            self.yspeed = 0
        else:
            self.y += self.yspeed
            self.shape.topleft = self.x, self.y

        self.frame_index += 0.1

    def render(self):
        draw_sprite(
            sprite_slime,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frame_index % (self.anim[-1] - self.anim[0] + 1))
            ],
            self.x - game.cam_x - self.offsx,
            self.y - game.cam_y - self.offsy,
        )

    def typeof(self):
        return "Slime"


def render_actors():
    for i in game.actor.values():
        for j in i:
            j.render()


class VerticallyMovingBlock(Actor):
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
        self.originalY = _y
        self.load_sprite(sprite_block)
        self.solid = True
        self.color = (200, 200, 200)
        self.frame_count = 0
        
        if not self.arr:
            return
        
        if self.arr.len() == 1:
            self.sprite_sheet = self.arr[0]
            self.load_sprite(self.sprite_sheet)

    def run(self):
        self.frame_count += 1

        self.y = self.originalY + math.sin(self.frame_count / 25) * 32

        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        draw_sprite(sprite_block, self.frame[0], self.x - game.cam_x, self.y - game.cam_y)

    def typeof(self):
        return "Block"

    def debug(self):
        pygame.draw.rect(
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
    def __init__(self, _x, _y, _arr=None):
        super().__init__(_x, _y, _arr=None)
        self.originalX = _x
        self.x = _x
        self.y = _y
        self.w = 16
        self.h = 16
        self.arr = _arr
        self.shape = pygame.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_block)
        self.solid = True
        self.color = (200, 200, 200)
        self.frame_count = 0
        
        if not self.arr:
            return
        
        if self.arr.len() == 1:
            self.sprite_sheet = self.arr[0]
            self.load_sprite(self.sprite_sheet)

    def run(self):
        self.frame_count += 1

        self.x = self.originalX + math.sin(self.frame_count / 25) * 32

        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        draw_sprite(sprite_block, self.frame[0], self.x - game.cam_x, self.y - game.cam_y)

    def typeof(self):
        return "Block"

    def debug(self):
        pygame.draw.rect(
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
        self.solid_offs_x = 0
        self.solid_offs_y = 0
        self.shape = pygame.Rect(self.x, self.y, self.w, self.h)
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
                    self.solid_offs_x = 0
                    self.solid_offs_y = 8
                    self.shape.w = 16
                    self.shape.h = 8
                
                if self.sort == 3:
                    self.solid_offs_x = 0
                    self.solid_offs_y = 0
                    self.shape.w = 8
                    self.shape.h = 16
                
                if self.sort == 4:
                    self.solid_offs_x = 8
                    self.solid_offs_y = 0
                    self.shape.w = 8
                    self.shape.h = 16
            
            if len(self.arr) >= 2:
                self.sprite_sheet = self.arr[1]
                self.load_sprite(self.sprite_sheet)
            
            if len(self.arr) >= 3:
                self.frame_index = self.arr[2]
            
            if len(self.arr) >= 4:
                self.solid = self.arr[3]
                
                if not self.solid:
                    self.color = (200, 200, 200, 90)
                    

    def run(self):
        self.shape.x = self.x + self.solid_offs_x
        self.shape.y = self.y + self.solid_offs_y

    def render(self):
        pass
    
    def debug(self):
        draw_sprite(
            self.sprite_sheet,
            self.frame[self.frame_index],
            self.x - game.cam_x,
            self.y - game.cam_y,
        )

    def typeof(self):
        return "Block"


class Tux(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.frame = []
        self.walk_right = [0.0, 3.0]
        self.walk_up = [4.0, 7.0]
        self.walk_down = [8.0, 11.0]
        self.walk_left = [12.0, 15.0]
        self.stand_right = [0]
        self.stand_left = [12]
        self.stand_up = [4]
        self.stand_down = [8]
        self.anim = self.walk_right
        self.stand_still = self.stand_right
        self.xspeed = 0
        self.yspeed = 0
        self.autocon = False
        self.idle = False
        self.step_count = 0
        self.shape = pygame.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_tux)
        self.solid = False
        self.color = (0, 255, 0)
        game.game_player = self
        self.animations = []

        if not arr:
            return

    def run(self):
        """if (keyboard.is_pressed(RIGHT) or keyboard.is_pressed(LEFT)) and (keyboard.is_pressed(UP) or keyboard.is_pressed(DOWN)):
            if keyboard.is_pressed(RIGHT):
                self.anim = self.walk_right
                self.stand_still = self.stand_right
            if keyboard.is_pressed(LEFT):
                self.anim = self.walk_left
                self.stand_still = self.stand_left"""


        if not keyboard.is_held(RIGHT) or not keyboard.is_held(LEFT):
            self.xspeed = 0

        if not keyboard.is_held(UP) or not keyboard.is_held(DOWN):
            self.yspeed = 0
        
        
        if keyboard.is_pressed(RIGHT):
            self.animations.append("right")
        if keyboard.is_pressed(LEFT):
            self.animations.append("left")
        if keyboard.is_pressed(UP):
            self.animations.append("up")
        if keyboard.is_pressed(DOWN):
            self.animations.append("down")
        
        if keyboard.is_released(RIGHT):
            if "right" in self.animations:
                self.animations.remove("right")
        if keyboard.is_released(LEFT):
            if "left" in self.animations:
                self.animations.remove("left")
        if keyboard.is_released(UP):
            if "up" in self.animations:
                self.animations.remove("up")
        if keyboard.is_released(DOWN):
            if "down" in self.animations:
                self.animations.remove("down")

        print(self.animations)
        
        if keyboard.is_held(RIGHT):
            self.xspeed = 1
            if len(self.animations) != 0:
                if self.animations[0] == "right":
                    self.anim = self.walk_right
                    self.stand_still = self.stand_right

        if keyboard.is_held(LEFT):
            self.xspeed = -1
            if len(self.animations) != 0:
                if self.animations[0] == "left":
                    self.anim = self.walk_left
                    self.stand_still = self.stand_left

        if keyboard.is_held(UP):
            self.yspeed = -1
            if len(self.animations) != 0:
                if self.animations[0] == "up":
                    self.anim = self.walk_up
            
                    self.stand_still = self.stand_up

        if keyboard.is_held(DOWN):
            self.yspeed = 1
            if len(self.animations) != 0:
                if self.animations[0] == "down":
                    self.anim = self.walk_down
                
                    self.stand_still = self.stand_down

        #print(self.animations)

        if keyboard.is_held(UP) and keyboard.is_held(DOWN):
            self.yspeed = 0
        
        if keyboard.is_held(RIGHT) and keyboard.is_held(LEFT):
            self.xspeed = 0

        if keyboard.is_pressed(RIGHT) or keyboard.is_pressed(LEFT) or keyboard.is_pressed(UP) or keyboard.is_pressed(DOWN):
            self.step_count += 1
            
            if self.step_count % 2 == 0:
                self.frame_index = 1
            else:
                self.frame_index = 3

        #print(self.animations)
        # Attempt to move in the x-axis by xspeed
        
        if collision_check(pygame.Rect(self.shape.x + self.xspeed, self.shape.y, self.shape.w, self.shape.h)):
            self.xspeed = 0
        else:
            self.x += self.xspeed
            self.shape.topleft = self.x, self.y
        
        # Attempt to move in the y-axis by yspeed
        
        if collision_check(pygame.Rect(self.shape.x, self.shape.y + self.yspeed, self.shape.w, self.shape.h)):
            self.yspeed = 0
        else:
            self.y += self.yspeed
            self.shape.topleft = self.x, self.y

        if self.xspeed == self.yspeed == 0:
            self.anim = self.stand_still

        self.frame_index += 0.14

        #print(self.animations)

    def render(self):
        draw_sprite(
            sprite_tux,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frame_index % (self.anim[-1] - self.anim[0] + 1))
            ],
            self.shape.x - game.cam_x,
            self.shape.y - game.cam_y,
        )

    def debug(self):
        pygame.draw.rect(
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

    def typeof(self):
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
        self.step_count = 0
        self.shape = pygame.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_soul, 8, 8)

        self.solid = False
        self.color = (0, 255, 0)
        game.game_player = self

        if not _arr:
            return

    def run(self):
        if not keyboard.is_held(RIGHT) or not keyboard.is_held(LEFT):
            self.xspeed = 0

        if not keyboard.is_held(UP) or not keyboard.is_held(DOWN):
            self.yspeed = 0

        if keyboard.is_held(RIGHT):
            self.xspeed = 1

        if keyboard.is_held(LEFT):
            self.xspeed = -1

        if keyboard.is_held(UP):
            self.yspeed = -1

        if keyboard.is_held(DOWN):
            self.yspeed = 1

        # Attempt to move in the x-axis by xspeed
        
        if collision_check(pygame.Rect(self.shape.x + self.xspeed, self.shape.y, self.shape.w, self.shape.h)):
            self.xspeed = 0
        else:
            self.x += self.xspeed
            self.shape.topleft = self.x, self.y
        
        # Attempt to move in the y-axis by yspeed

        if collision_check(pygame.Rect(self.shape.x, self.shape.y + self.yspeed, self.shape.w, self.shape.h)):
            self.yspeed = 0
        else:
            self.y += self.yspeed
            self.shape.topleft = self.x, self.y

        if game.hurt_timer > 0:
            self.anim = self.invisible
        else:
            self.anim = self.visible

        self.frame_index += 0.14

    def render(self):
        draw_sprite(
            sprite_soul,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frame_index % (self.anim[-1] - self.anim[0] + 1))
            ],
            self.shape.x - game.cam_x,
            self.shape.y - game.cam_y,
        )

    def debug(self):
        pygame.draw.rect(
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

    def typeof(self):
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
        self.shape = pygame.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_bullet, 4, 4)
        
        if self.arr is not None:
            self.xspeed = self.arr[0][0]
            self.yspeed = self.arr[0][1]

    def debug(self):
        pygame.draw.rect(
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
        self.frame_index += 0.1

        if game.game_player.shape.colliderect(self.shape):
            if game.hurt_timer == 0:
                game.health -= 1
                game.hurt_timer = 60
                
        
        self.x += self.xspeed
        self.y += self.yspeed
        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        # pass

        draw_sprite(
            sprite_bullet,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frame_index % (self.anim[-1] - self.anim[0] + 1))
            ],
            self.x - game.cam_x,
            self.y - game.cam_y,
        )

    def typeof(self):
        return "Bullet"

animation = {"events": []}

class Attack:
    def __init__(self, _opponent, _timer=0):
        self.opponent = _opponent
        self.timer = 0

    def run(self):
        self.timer += 1
        for i in animation["events"]:
            if i["start"] <= self.timer < i["stop"]:
                spawn = i["spawn"]
                for j in range(0, len(spawn)):
                    entity = spawn[j]["entity"]
                    new_actor(entity["object"], entity["x"], entity["y"], entity["arr"], "actorlayer")

    def construct_attack(self, _x, _y, _xspace, _yspace, _start, _wait, _number, _speed):
        for i in range(0, _number):
            dic = {
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

            animation["events"].append(dic)

    def construct_circle_attack(self, x, y, r, start, wait, number, speed):
        for i in range(0, number):
            dv = 2 * math.pi / number
            dic = {
                "start": start + i * wait,
                "stop": start + i * wait + 1,
                "function": 0,
                "spawn": [
                    {
                        "entity": {
                            "object": Bullet,
                            "x": x + math.cos(dv * i) * r,
                            "y": y + math.sin(dv * i) * r,
                            "arr": [(speed[0], speed[1])],
                        },
                    }
                ],
            }
            animation["events"].append(dic)

class NPC(Actor):
    def __init__(self, _x, _y, _arr = None):
        super().__init__(_x, _y, _arr = None)
        self.x = _x
        self.y = _y
        self.arr = _arr
        if self.arr is not None:
            if len(self.arr) >= 1:
                self.sprite_sheet = self.arr[0]
                self.load_sprite(self.sprite_sheet)
            if len(self.arr) >= 2:
                self.dialogue = self.arr[1]
        
    def run(self):
        player_vec = pygame.math.Vector2(game.game_player.x, game.game_player.y)
        NPC_vec = pygame.math.Vector2(self.x, self.y)
        distance = (player_vec - NPC_vec).magnitude()
        if distance <= 16 and game.text_boxes == []:
            if(keyboard.is_pressed(ACCEPT)):
                game.text_boxes.append(TextBox(10, 10, Dialogue))
                
    def render(self):
        # pass

        draw_sprite(
            self.sprite_sheet,
            self.frame[
                0
            ],
            self.x - game.cam_x,
            self.y - game.cam_y,
        )