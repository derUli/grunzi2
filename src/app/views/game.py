""" Main game class """
from arcade import FACE_LEFT, FACE_RIGHT

from app.constants.input.keyboard import KEY_LEFT, KEY_RIGHT, KEY_JUMP, KEY_SPRINT
from app.utils.level import Level
from app.views.view import View


class Game(View):
    """ Main game class """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._level = None
        self._move_horizontal = None
        self._jump = False
        self._sprint = False

    def setup(self, root_dir: str):
        """ Setup game"""

        super().setup(root_dir)

        self._level = Level()
        self.window.set_mouse_visible(False)

    def setup_level(self, map_name: str):
        """ Setup level """

        self._level.setup(self._root_dir, map_name)

    def on_update(self, delta_time: float):
        """ On level update """
        self._level.update(
            move_horizontal=self._move_horizontal,
            jump=self._jump,
            sprint=self._sprint
        )

        if self._jump:
            self._jump = False

    def on_draw(self):
        """ On draw """

        self.clear()
        self._level.draw()
        self.window.draw_after()

    def on_key_press(self, symbol: int, modifiers: int):
        """ On key press """

        if symbol in KEY_LEFT:
            self._move_horizontal = FACE_LEFT

        if symbol in KEY_RIGHT:
            self._move_horizontal = FACE_RIGHT

        if symbol in KEY_JUMP:
            self._jump = True

        if symbol in KEY_SPRINT:
            self._sprint = True

    def on_key_release(self, _symbol: int, _modifiers: int):
        """ On key release"""

        if self._move_horizontal == FACE_LEFT and _symbol in KEY_LEFT:
            self._move_horizontal = None
        if self._move_horizontal == FACE_RIGHT and _symbol in KEY_RIGHT:
            self._move_horizontal = None

        if self._sprint and _symbol in KEY_SPRINT:
            self._sprint = False
