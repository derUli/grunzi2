""" Main game class """
import arcade

from app.utils.level import Level
from app.views.view import View


class Game(View):
    """ Main game class """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self._level = None

    def setup(self, root_dir: str):
        """ Setup game"""

        super().setup(root_dir)

        self._level = Level()

    def setup_level(self, map_name: str):
        self._level.setup(self._root_dir, map_name)

    def on_update(self, delta_time: float):
        self._level.update()

    def on_draw(self):
        """ On draw """

        self.clear()
        self._level.draw()
        self.window.draw_after()
