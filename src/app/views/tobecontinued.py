""" To be continued screen"""


import arcade
from app.views.view import View


class ToBeContinued(View):
    """ To be continued screen"""

    def setup(self, root_dir: str):
        """ Setup logo screen """

        super().setup(root_dir)
        self.window.set_mouse_visible(False)
        arcade.set_background_color(arcade.color.WHITE)
        print('Sort')

        return self

    def on_draw(self):
        """ On draw """
        self.clear()