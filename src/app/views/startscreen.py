import gettext
import os

import arcade
from arcade import View, Window

from app.constants.input.keyboard import KEY_ESCAPE, KEY_CONFIRM

_ = gettext.gettext

BACKGROUND_COLOR = (58, 154, 230, 255)
FONT_SIZE = 20
FADE_SPEED = 5
FADE_MAX = 255
MUSIC_FADE_SPEED = 0.01

SCENE_LAYER_FADEIN = 'fadein'


class StartScreen(View):
    def __init__(self, window: Window | None = None) -> None:
        """ Constructor """

        super().__init__(window)
        self._text = None
        self._fade_sprite = None
        self._scene = arcade.Scene()
        self._music = None

    def setup(self, root_dir):
        """ Setup the start screen """

        # Background color
        arcade.set_background_color(BACKGROUND_COLOR)

        # Text
        text = _('Press any key to start')

        # TODO

        # if controller then
        # text = _('Anderer Text')
        self._text = arcade.Text(text=text, x=0, y=0, font_size=FONT_SIZE)

        # TODO: Particle Effekte

        music = arcade.load_sound(
            os.path.join(root_dir, 'resources', 'music', 'DeepSpace.mp3'),
            streaming=True
        )
        self._music = music.play(loop=True)

    def on_update(self, delta_time: float):
        """ On update """

        self._text.x = (self.window.width / 2) - (self._text.content_width / 2)
        self._text.y = self._text.content_height

        """ On update scene """
        if self._fade_sprite is not None:

            self._fade_sprite.alpha = min(self._fade_sprite.alpha + FADE_SPEED, 255)

            if self._fade_sprite.alpha >= FADE_MAX:
                self._fade_sprite.alpha = FADE_MAX

            if self._music:
                self._music.volume = max(self._music.volume - MUSIC_FADE_SPEED, 0)
                if self._music.volume <= 0:
                    self._music.pause()
                    self._music = None

                    print('TODO: start game')

    def on_draw(self):
        """ On draw"""

        # Clear screen
        self.clear()

        # Draw text
        self._text.draw()

        # Draw scene
        self._scene.draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard input """

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
