""" Level """
import math
import os

import arcade

from app.constants.layers import LAYER_BACKDROP, LAYER_PLAYER

VIEWPORT_BASE_H = 1080


class Level:
    """ Level """

    def __init__(self):
        """ Constructor"""

        self.scene = None
        self.tilemap = None
        self._camera = None

    def setup(self, root_dir: str, map_name: str):
        """ Setup level """

        path = os.path.join(root_dir, 'resources', 'maps', f"{map_name}.tmx")

        self.load_tilemap(path)

        w, h = arcade.get_window().get_size()
        zoom = h / VIEWPORT_BASE_H
        self._camera = arcade.camera.Camera2D(
            zoom=1,
            position=(
                w,
                self.scene[LAYER_BACKDROP][0].top
            )
        )

    def load_tilemap(self, path):
        """ Load tilemap """

        self.tilemap = arcade.load_tilemap(path)
        self.scene = arcade.Scene.from_tilemap(self.tilemap)

    def update(self):
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

        player = self.scene[LAYER_PLAYER][0]

        x, y = player.center_x, player.center_y

        x = max(x, w / 2)

        y += h / 2
        y -= player.height / 2

        zoom = round(self._camera.zoom, 2)

        x += (1 - zoom) * x
        y += (1 - zoom) * y

        self._camera.position = arcade.math.lerp_2d(
            self._camera.position, (x, y), camera_speed
        )

    def draw(self):
        self._camera.use()
        self.scene.draw()
