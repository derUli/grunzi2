""" Level """
import os

import arcade
import pyglet
from arcade import FACE_RIGHT, FACE_LEFT

from app.constants.layers import LAYER_PLAYER, LAYER_WALL

VIEWPORT_BASE_H = 1080
PLAYER_MOVE_SPEED = 5
PLAYER_JUMP_SPEED = 30
PLAYER_MOVE_ANGLE = 2

MODIFIER_WALK = 1.0
MODIFIER_SPRINT = 1.3

GRAVITY_SLOWMO = 0.0025
GRAVITY_DEFAULT = 1

ALPHA_SPEED = 1
ALPHA_MAX = 255


class Level:
    """ Level """

    def __init__(self):
        """ Constructor"""

        self._scene = None
        self.tilemap = None
        self._camera = None
        self._physics_engine = None
        self._can_walk = False

    def setup(self, root_dir: str, map_name: str):
        """ Setup level """

        path = os.path.join(root_dir, 'resources', 'maps', f"{map_name}.tmx")

        self.load_tilemap(path)

        w, h = arcade.get_window().get_size()
        self._camera = arcade.camera.Camera2D()
        self.scroll_to_player()

        self.setup_physics_engine()

        self.wait_for_begin()

    def setup_physics_engine(self):
        self._physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            ladders=None,
            walls=self._scene[LAYER_WALL],
            gravity_constant=GRAVITY_SLOWMO
        )

    def load_tilemap(self, path):
        """ Load tilemap """

        w, h = arcade.get_window().get_size()
        zoom = h / VIEWPORT_BASE_H

        self.tilemap = arcade.load_tilemap(path, scaling=zoom)
        self._scene = arcade.Scene.from_tilemap(self.tilemap)

        self.player.alpha = 0

    def update(
            self,
            move_horizontal: int = None,
            jump: bool = False,
            sprint: bool = False
    ):
        if jump:
            self.jump()

        if move_horizontal == FACE_RIGHT:
            self.move_right(sprint)
        elif move_horizontal == FACE_LEFT:
            self.move_left(sprint)
        else:
            self.move_stop()

        self.player.alpha = min(self.player.alpha + ALPHA_SPEED, 255)
        self._physics_engine.update()
        self.scroll_to_player()

    def scroll_to_player(self, camera_speed=1):
        """
        Scroll the window to the player.
        This method will attempt to keep the player at least VIEWPORT_MARGIN
        pixels away from the edge.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """
        w, h = arcade.get_window().get_size()

        player = self.player

        x, y = player.position

        self._camera.position = arcade.math.lerp_2d(
            self._camera.position, (x, y), camera_speed
        )

    def draw(self):
        """ Draw level """

        self._camera.use()
        self._scene.draw()


    def move_left(self, sprint: bool = False):

        if not self._can_walk:
            return

        modifier = MODIFIER_WALK

        if sprint:
            modifier = MODIFIER_SPRINT

        self.player.change_x = -PLAYER_MOVE_SPEED * modifier
        self.player.angle -= PLAYER_MOVE_ANGLE * modifier

        if self.player.angle <= 0 :
            self.player.angle = 360 - abs(self.player.angle)

    def move_right(self, sprint: bool = False):

        if not self._can_walk:
            return

        modifier = MODIFIER_WALK

        if sprint:
            modifier = MODIFIER_SPRINT

        self.player.change_x = PLAYER_MOVE_SPEED * modifier
        self.player.angle += PLAYER_MOVE_ANGLE * modifier

        if self.player.angle > 360:
            self.player.angle = self.player.angle - 360

    def move_stop(self):
        if not self._can_walk:
            return

        self.player.change_x = 0

    def jump(self):
        if not self._physics_engine.can_jump(y_distance=10):
            return

        self.player.change_y = PLAYER_JUMP_SPEED

    @property
    def player(self):
        """ The player sprite """
        return self._scene[LAYER_PLAYER][0]

    def wait_for_begin(self, dt: float = 0.0):
        """ Wait for begin of level """
        if self._physics_engine.can_jump():
            self._can_walk = True
            self._physics_engine.gravity_constant = GRAVITY_DEFAULT
            return

        pyglet.clock.schedule_once(self.wait_for_begin, 1 / 4)
