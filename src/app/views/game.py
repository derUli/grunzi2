""" Main game class """
import arcade

from app.views.view import View


class Game(View):
    """ Main game class """

    def __init__(self):
        """ Constructor """

        super().__init__()

    def setup(self, root_dir: str):
        """ Setup game"""

        super().setup(root_dir)

        arcade.set_background_color(arcade.color.RED)

    def on_draw(self):
        """ On draw """

        self.clear()
        self.window.draw_after()
