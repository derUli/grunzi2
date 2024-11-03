""" The main menu """

import gettext
import logging
import os
import random
import webbrowser

import arcade
from arcade import View, Window

from app.constants.input.controllers import KEY_START, KEY_BACK
from app.constants.input.keyboard import KEY_ESCAPE, KEY_CONFIRM
from app.constants.input.mouse import BUTTON_LEFT_CLICK

_ = gettext.gettext

BACKGROUND_COLOR = (58, 154, 230, 255)
FONT_SIZE = 20
FONT_SIZE_TITLE = 80
FADE_SPEED = 5
FADE_MAX = 255
MUSIC_FADE_SPEED = 0.01
MARGIN = 10

SCENE_LAYER_FADEIN = 'fadein'
SCENE_LAYER_ICON = 'icon'
SCENE_LAYER_PARTICLES = 'particles'

PARTICLE_SPEED = 2

PARTICLE_COLORS = [
    (228, 255, 4, 200),
    (210, 210, 210, 200),
    (111, 186, 241, 200)
]
PARTICLES_SIZE_RANGE = 8
PARTICLES_COUNT = 500

URL_ITCH_IO = 'https://hog-games.itch.io/'


class StartScreen(View):
    """ The main menu """

    def __init__(self, window: Window | None = None) -> None:
        """ Constructor """

        super().__init__(window)
        self._text_start = None
        self._text_title = None
        self._fade_sprite = None
        self._scene = arcade.Scene()
        self._icon_itch_io = None
        self._music = None
        self._last_hover = None

    def setup(self, root_dir: str):
        """ Setup the start screen """

        # Background color
        arcade.set_background_color(BACKGROUND_COLOR)
        self.window.set_mouse_visible(not any(self.window.controllers))

        # Text
        self.setup_text()
        self.setup_particles()
        self.setup_icons(root_dir)

        # Play music
        self.setup_music(root_dir)

    def setup_text(self):
        """ Setup text """

        text = _('Press SPACE key to start')

        if any(self.window.controllers):
            text = _('Press START button to start')

        # if controller then
        # text = _('Anderer Text')
        self._text_start = arcade.Text(text=text, x=0, y=0, font_size=FONT_SIZE)
        self._text_title = arcade.Text(
            text=self.window.caption,
            x=0,
            y=0,
            font_size=FONT_SIZE_TITLE
        )

    def setup_icons(self, root_dir: str):
        """ Setup menu icons """

        self._icon_itch_io = arcade.sprite.Sprite(
            path_or_texture=os.path.join(root_dir, 'resources', 'images', 'ui', 'itch-io.jpg'),
            x=0,
            y=0
        )

        self._scene.add_sprite(SCENE_LAYER_ICON, self._icon_itch_io)

    def setup_music(self, root_dir: str):
        """ Play music """
        music = arcade.load_sound(
            os.path.join(root_dir, 'resources', 'music', 'DeepSpace.mp3'),
            streaming=True
        )
        self._music = music.play(loop=True, volume=1)

    def setup_particles(self):
        """ Setup article animation """

        try:
            self._scene.remove_sprite_list_by_name(SCENE_LAYER_PARTICLES)
        except KeyError:
            pass

        for i in range(0, PARTICLES_COUNT):
            sprite = arcade.sprite.SpriteCircle(
                color=random.choice(PARTICLE_COLORS),
                soft=True,
                radius=random.randint(1, PARTICLES_SIZE_RANGE)
            )
            sprite.center_x = random.randint(0, self.window.width)
            sprite.center_y = random.randint(0, self.window.height)
            self._scene.add_sprite(SCENE_LAYER_PARTICLES, sprite)

    def on_update(self, delta_time: float):
        """ On update """

        self.on_update_particles()
        self._text_start.x = (self.window.width / 2) - (self._text_start.content_width / 2)
        self._text_start.y = self._text_start.content_height

        self._text_title.x = (self.window.width / 2) - (self._text_title.content_width / 2)
        self._text_title.y = self.window.height / 2

        self._icon_itch_io.right = self.window.width - MARGIN
        self._icon_itch_io.bottom = MARGIN

        # On fading in
        if self._fade_sprite is not None:

            self._fade_sprite.alpha = min(self._fade_sprite.alpha + FADE_SPEED, 255)

            if self._music:
                self._music.volume = max(self._music.volume - MUSIC_FADE_SPEED, 0)
                if self._music.volume <= 0:
                    self._music.pause()
                    self._music = None

                    logging.info('TODO: start game')

    def on_update_particles(self):
        """ Update particles """
        particles = self._scene[SCENE_LAYER_PARTICLES]
        for particle in particles:
            particle.center_x -= PARTICLE_SPEED

            if particle.right < 0:
                particle.center_x = self.window.width + particle.width
                particle.center_y = random.randint(0, self.window.height)

    def on_draw(self):
        """ On draw"""

        # Clear screen
        self.clear()

        # Draw scene
        self._scene.draw()

        # Draw text
        self._text_title.draw()
        self._text_start.draw()

        if SCENE_LAYER_FADEIN in self._scene:
            self._scene[SCENE_LAYER_FADEIN].draw()

    def on_key_press(self, symbol: int, modifiers: int):
        """ Handle keyboard input """

        if symbol in KEY_ESCAPE:
            self.on_exit()

        if symbol in KEY_CONFIRM and self._fade_sprite is None:
            self.on_start_game()

    def on_resize(self, width, height):
        """ On resize """

        logging.info("Resize to %s", (width, height))

        self.setup_particles()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int) -> bool | None:
        """ Handle mouse movement """

        if self._last_hover:
            if not self._last_hover.collides_with_point((x, y)):
                self._last_hover.scale = 1.0
                self._last_hover = None
            return

        sprites = [
            self._icon_itch_io
        ]

        for sprite in sprites:
            if sprite.collides_with_point((x, y)):
                logging.info('Mouse entering item')

                self._last_hover = sprite
                self._last_hover.scale = 1.02
                break

    def on_mouse_press(self, x, y, button, modifiers) -> bool | None:
        """ Handle mouse press """

        if button not in BUTTON_LEFT_CLICK:
            return

        if not self._last_hover:
            self.on_start_game()
            return

        if self._last_hover == self._icon_itch_io:
            self.on_itch_io()

    def on_button_press(self, joystick, key) -> None:
        """ On controller button press """
        if key == KEY_START:
            self.on_start_game()
        elif key == KEY_BACK:
            self.on_exit()

    def on_start_game(self) -> None:
        """ On start new game """

        self.window.set_mouse_visible(False)

        self._fade_sprite = arcade.sprite.SpriteSolidColor(
            width=self.window.width,
            height=self.window.height,
            color=BACKGROUND_COLOR
        )
        self._fade_sprite.center_x = self.window.width / 2
        self._fade_sprite.center_y = self.window.height / 2

        self._fade_sprite.alpha = 0
        self._scene.add_sprite(SCENE_LAYER_FADEIN, self._fade_sprite)

    @staticmethod
    def on_itch_io() -> None:
        """ On open itch.io """

        webbrowser.open_new_tab(URL_ITCH_IO)

    @staticmethod
    def on_exit() -> None:
        """ On exit game """

        arcade.exit()
