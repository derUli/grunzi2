""" Main game class """
from arcade import FACE_LEFT, FACE_RIGHT

from app.constants.input.keyboard import KEY_LEFT, KEY_RIGHT
from app.utils.level import Level
from app.views.view import View


class Game(View):
    """ Main game class """

    def __init__(self):
        """ Constructor """
        super().__init__()
        self._level = None
        self._move_horizontal = None

    def setup(self, root_dir: str):
        """ Setup game"""

        super().setup(root_dir)

        self._level = Level()
        self.window.set_mouse_visible(False)

    def setup_level(self, map_name: str):
        self._level.setup(self._root_dir, map_name)

    def on_update(self, delta_time: float):
        """ On level update """
        self._level.update(move_horizontal=self._move_horizontal)

    def on_draw(self):
        """ On draw """

        self.clear()
        self._level.draw()
        self.window.draw_after()


    def on_key_press(self, symbol: int, modifiers: int):
        """ On key press """

        if symbol in KEY_LEFT:
            self._move_horizontal = FACE_LEFT
        elif symbol in KEY_RIGHT:
            self._move_horizontal = FACE_RIGHT
        else:
            self._move_horizontal = None


    def on_key_release(self, _symbol: int, _modifiers: int):
        """ On key release"""

        horizontal_movement_keys = KEY_LEFT + KEY_RIGHT
        if self._move_horizontal and _symbol in horizontal_movement_keys:
            self._move_horizontal = None