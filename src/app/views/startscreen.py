import arcade
from arcade import View, Window

import gettext

from app.constants.input.keyboard import KEY_ESCAPE, KEY_CONFIRM

_ = gettext.gettext

BACKGROUND_COLOR = (58, 154, 230, 255)
FONT_SIZE = 20
FADE_SPEED = 5
FADE_MAX = 255

SCENE_LAYER_FADEIN = 'fadein'

class StartScreen(View):
    def __init__(self, window: Window | None = None) -> None:
        """ Constructor """

        super().__init__(window)
        self._text = None
        self._fade_sprite = None
        self._scene = arcade.Scene()

    def setup(self):
        """ Setup the start screen """

        # Background color
        arcade.set_background_color(BACKGROUND_COLOR)

        # Text
        text =  _('Press any key to start')

        # TODO

        # if controller then
        # text = _('Anderer Text')
        self._text = arcade.Text(text = text, x = 0, y = 0, font_size = FONT_SIZE)
        self._text.x = (self.window.width / 2) - (self._text.content_width / 2)
        self._text.y = self._text.content_height

        # TODO: Particle Effekte

    def on_update(self, delta_time: float):
        if self._fade_sprite is not None and self._fade_sprite.alpha < FADE_MAX:
            self._fade_sprite.alpha += FADE_SPEED

            if self._fade_sprite.alpha  > FADE_MAX:
                self._fade_sprite.alpha = FADE_MAX

                print('TODO: Spiel starten')


    def on_draw(self):
        """ On draw"""
        self.clear()
        self._text.draw()
        self._scene.draw()


    def on_key_press(self, symbol: int, modifiers: int):
        if symbol in KEY_ESCAPE:
            self.on_exit()

        if symbol in KEY_CONFIRM and self._fade_sprite is None:
            self.on_start_game()


    @staticmethod
    def on_exit() -> None:
        """ On exit game """

        arcade.exit()

    def on_start_game(self) -> None:
        """ On start new game """

        self._fade_sprite = arcade.sprite.SpriteSolidColor(
            width=self.window.width,
            height=self.window.height,
            color=BACKGROUND_COLOR
        )
        self._fade_sprite.center_x = self.window.width / 2
        self._fade_sprite.center_y = self.window.height / 2

        self._fade_sprite.alpha = 0
        self._scene.add_sprite(SCENE_LAYER_FADEIN, self._fade_sprite)