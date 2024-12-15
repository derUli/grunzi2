""" To be continued screen"""


import arcade

from app.constants.fonts import FONT_MARKER_FELT
from app.constants.input.controllers import KEY_START
from app.constants.input.keyboard import KEY_CONFIRM
from app.views.view import View

FONT_SIZE = 60

SCENE_LAYER_TEXT = 'Text'

class ToBeContinued(View):

    def __init__(self):
        """ To be continued screen """

        super().__init__()

        self._text_completed = None
        self.window = None
        self.background_color = arcade.csscolor.WHITE

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

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard input """


        if symbol in KEY_CONFIRM and self._fade_sprite is None:
            self.on_main_menu()

    def on_update(self, delta_time: float):
        w, h = self.window.get_size()
        self._text_completed.center_x = w / 2
        self._text_completed.center_y = h / 2
        self._scene[SCENE_LAYER_TEXT].visible = True

    def on_draw(self):
        """ On draw """

        self.clear()
        self._scene.draw()

    def on_button_press(self, joystick, key) -> None:
        """ On controller button press """

        if key == KEY_START:
            self.on_main_menu()



    def on_main_menu(self):
        from app.views.mainmenu import MainMenu
        self.window.show_view(MainMenu().setup(self._root_dir))
