""" Main game class """
from arcade import FACE_LEFT, FACE_RIGHT

from app.constants.input.controllers import KEY_A, LEFTSTICK, AXIS_RIGHT, AXIS_LEFT
from app.constants.input.keyboard import KEY_LEFT, KEY_RIGHT, KEY_JUMP, KEY_SPRINT
from app.utils.audiovolumes import AudioVolumes
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

        self.window.set_mouse_visible(False)
        super().setup(root_dir)

        self._level = Level()
        self.window.set_mouse_visible(False)

    def setup_level(self, map_name: str):
        """ Setup level """

        self._level.setup(self._root_dir, map_name, self.window.audio_volumes)

    def on_update(self, delta_time: float):
        """ On level update """
        self._level.update(
            delta_time=delta_time,
            window=self.window,
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

    def on_stick_motion(self, joystick, stick, value):
        """ On stick motion """

        if stick == LEFTSTICK:
            x, y = value
            x, y = round(x), round(y)

            if x == AXIS_RIGHT:
                self._move_horizontal = FACE_RIGHT
            elif x == AXIS_LEFT:
                self._move_horizontal = FACE_LEFT
            else:
                self._move_horizontal = None

    def on_button_press(self, joystick, key) -> None:
        """ On controller button press """

        if key == KEY_A:
            self._jump = True

        if key == LEFTSTICK:
            self._sprint = True

    def on_button_release(self, joystick, key):
        """ On controller button release """

        if key == KEY_LEFT:
            self._sprint = False
