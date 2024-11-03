""" Logo splash screen"""
import os

import arcade
import pyglet
from arcade import View

from app.views.startscreen import StartScreen

SCENE_LAYER_LOGO = 'Logo'

LOGO_LENGTH = 3


class Logo(View):
    """ Logo splash screen"""

    def __init__(self):
        """ Constructor """

        super().__init__()
        self._root_dir = None
        self.scene = None

    def setup(self, root_dir: str):
        """ Setup logo screen """

        arcade.set_background_color(arcade.color.WHITE)
        self._root_dir = root_dir
        logo_file = os.path.join(self._root_dir, 'resources', 'images', 'ui', 'hog-games.png')
        logo = arcade.sprite.Sprite(path_or_texture=logo_file, x=0, y=0)

        self.scene = arcade.scene.Scene()
        self.scene.add_sprite(SCENE_LAYER_LOGO, logo)

        # TODO: Fade in, play sound, fade out
        pyglet.clock.schedule_interval(self.show_startscreen, LOGO_LENGTH)

    def on_update(self, delta_time: float):
        """ On update """

        self.scene[SCENE_LAYER_LOGO][0].center_x = self.window.width / 2
        self.scene[SCENE_LAYER_LOGO][0].center_y = self.window.height / 2

    def on_draw(self):
        """ On draw """

        self.scene.draw()

    def show_startscreen(self, dt: float):
        """ Show StartScreen """

        view = StartScreen()
        view.setup(root_dir=self._root_dir)
        self.window.show_view(view)
