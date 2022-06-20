from .init import *

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

        game.cam_x = game.game_player.shape.x - (display_w / 2) + game.game_player.w / 2
        game.cam_y = game.game_player.shape.y - (display_H / 2) + game.game_player.h / 2

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
    game.unusedActors = game.actor
    game.actor = {"solid": [], "BG": [], "MG": [], "actorlayer": [], "FG": []}


def battle_mode():
    pass


def start_play():
    pass


def save_game():
    pass


def quit_game():
    pass
