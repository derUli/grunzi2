""" To be continued screen"""


import arcade

from app.constants.fonts import FONT_MARKER_FELT
from app.views.view import View

FONT_SIZE = 60

SCENE_LAYER_TEXT = 'Text'

class ToBeContinued(View):

    def __init__(self):
        self._text_completed = None
        self.window = None
        self.background_color = arcade.csscolor.WHITE
    """ To be continued screen"""

    def setup(self, root_dir: str):
        """ Setup logo screen """

        self.window = arcade.get_window()

        super().setup(root_dir)
        self.window.set_mouse_visible(False)

        self._text_completed = arcade.create_text_sprite(
            text=_('To be continued'),
            font_name=FONT_MARKER_FELT,
            font_size=FONT_SIZE,
            color=arcade.csscolor.BLACK,
            bold=True,
        )

        self._scene.add_sprite(SCENE_LAYER_TEXT, self._text_completed)
        self._scene[SCENE_LAYER_TEXT].visible = False

        return self

    def on_update(self, delta_time: float):
        w, h = self.window.get_size()
        self._text_completed.center_x = w / 2
        self._text_completed.center_y = h / 2
        self._scene[SCENE_LAYER_TEXT].visible = True

    def on_draw(self):
        """ On draw """

        self.clear()
        self._scene.draw()
