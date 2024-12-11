# pylint: disable=W0223

""" The Game window """

import logging
import os
import time

import arcade
import pyglet
import userpaths

from app.constants.gameinfo import DIRECTORY_GAME_NAME
from app.constants.input.keyboard import KEY_SCREENSHOT, KEY_TOGGLE_FULLSCREEN, KEY_TOGGLE_FPS
from app.constants.settings import SETTINGS_SIZE_MINIUM
from app.utils.audiovolumes import AudioVolumes
from app.utils.fpscounter import FPSCounter
from app.utils.string import label_value
from app.views.logo import Logo
from app.views.mainmenu import MainMenu

MARGIN = 10


class GameWindow(arcade.Window):
    """
    Main application class
    """

    def __init__(
            self,
            width: int = 1280,
            height: int = 720,
            fullscreen: bool = True,
            visible: bool = True,
            style: str | None = None,
            vsync: bool = True,
            draw_rate: int = 1 / 60,
            update_rate=1 / 60,
            center_window=False,
            antialiasing: bool = True,
            samples: int = 4,
            fixed_rate: float = 1 / 60

    ):
        """ Constructor """

        self._mode = None
        self._root_dir = None
        self._screen = None
        self._controller_manager = None
        self._controllers = []
        self._fps_counter = None
        self._audio_volumes = None

        # Call the parent class and set up the window
        super().__init__(
            width=width,
            height=height,
            title=_('Welcome to Amerre'),
            fullscreen=fullscreen,
            visible=visible,
            style=style,
            vsync=vsync,
            resizable=False,
            draw_rate=draw_rate,
            update_rate=update_rate,
            center_window=center_window,
            antialiasing=antialiasing,
            samples=samples,
            gc_mode='auto',
            fixed_rate=fixed_rate
        )

    def setup(
            self,
            root_dir: str,
            audio_volumes: AudioVolumes,
            show_intro: bool = True,
            show_fps: bool = False,
    ):
        """ Set up the main window here"""

        self._root_dir = root_dir
        self._audio_volumes = audio_volumes

        icon = pyglet.image.load(
            os.path.join(root_dir, 'resources', 'images', 'ui', 'icon.ico')
        )
        self.set_icon(icon)
        self.setup_fonts()
        self.setup_controllers()

        w, h = SETTINGS_SIZE_MINIUM
        self.set_minimum_size(w, h)

        if show_intro:
            view = Logo
        else:
            view = MainMenu

        if show_fps:
            arcade.enable_timings()
            self._fps_counter = FPSCounter().setup(self)

        self.show_view(view().setup(root_dir))

    @property
    def size(self):
        """ Window size """

        return self.width, self.height

    def setup_controllers(self):
        """ Setup controllers """

        self._controller_manager = pyglet.input.ControllerManager()
        controllers = self._controller_manager.get_controllers()
        for controller in controllers:
            logging.info(label_value('Controller connected', controller))

            controller.open()
            controller.push_handlers(self)

            self._controllers.append(controller)

        @self._controller_manager.event
        def on_connect(controller) -> None:
            """ On controller connect """

            logging.info(label_value('Controller connected', controller))

            controller.open()
            controller.push_handlers(self)

            self._controllers.append(controller)

        @self._controller_manager.event
        def on_disconnect(controller):
            """ On controller disconnect """

            logging.info(label_value('Controller disconnected', controller))
            controller.pop_handlers()
            controller.close()
            self._controllers.remove(controller)

    def setup_fonts(self):
        """ Load fonts """

        fonts = [
            'MarkerFelt.ttf',
            'consolamonobook.ttf'
        ]

        for font in fonts:
            arcade.load_font(
                os.path.join(
                    self._root_dir,
                    'resources',
                    'fonts',
                    font
                )
            )

    def on_button_press(self, joystick, key) -> None:
        """ On controller button pressed """

        if hasattr(self.current_view, 'on_button_press'):
            self.current_view.on_button_press(joystick, key)
        else:
            logging.debug(
                label_value(
                    self.current_view.__class__.__qualname__,
                    'on_button_press not implemented'
                )
            )

    def on_button_release(self, joystick, key) -> None:
        """ On controller button released """

        if hasattr(self.current_view, 'on_button_release'):
            self.current_view.on_button_release(joystick, key)
        else:
            logging.debug(
                label_value(
                    self.current_view.__class__.__qualname__,
                    'on_button_release not implemented'
                )
            )

    def on_stick_motion(self, joystick, stick, value):
        """ On stick motion """

        if hasattr(self.current_view, 'on_stick_motion'):
            self.current_view.on_stick_motion(joystick, stick, value)
        else:
            logging.debug(
                label_value(
                    self.current_view.__class__.__qualname__,
                    'on_stick_motion not implemented'
                )
            )

    def on_trigger_motion(self, joystick, stick, value):
        """ On stick motion """

        if hasattr(self.current_view, 'on_trigger_motion'):
            self.current_view.on_trigger_motion(joystick, stick, value)
        else:
            logging.debug(
                label_value(
                    self.current_view.__class__.__qualname__,
                    'on_trigger_motion not implemented'
                )
            )

    @property
    def controllers(self):
        """ Get controllers """

        return self._controllers

    def on_key_press(self, symbol: int, modifiers: int):
        """ On keyboard key presssed """

        if symbol in KEY_SCREENSHOT:
            self.on_screenshot()
        if symbol in KEY_TOGGLE_FULLSCREEN:
            self.set_fullscreen(not self.fullscreen)
        if symbol in KEY_TOGGLE_FPS:
            self.on_toggle_fps()

    def on_screenshot(self):
        """ Save a screenshot """

        screenshot_dir = str(os.path.join(userpaths.get_my_pictures(), DIRECTORY_GAME_NAME))

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        filename = os.path.join(screenshot_dir, time.strftime("%Y%m%d-%H%M%S") + '.jpg')

        start = time.time()
        image = arcade.get_image().convert('RGB')
        image.save(filename, subsampling=0, quality=100)
        end = time.time() - start

        logging.info(f"Screenshot saved as {filename} in {end} seconds")

        sound = arcade.load_sound(
            os.path.join(self._root_dir, 'resources', 'sounds', 'common', 'screenshot.mp3')
        )
        sound.play(volume=self._audio_volumes.volume_sound)

        return filename

    def on_toggle_fps(self):
        """ Toggle fps counter """
        if self._fps_counter:
            arcade.disable_timings()
            self._fps_counter = None
        else:
            arcade.enable_timings()
            self._fps_counter = FPSCounter().setup(self)

    def on_update(self, delta_time: float):
        """ On update """

        if self._fps_counter:
            self._fps_counter.update()

    def draw_after(self):
        """ Draw after view """

        if self._fps_counter:
            self._fps_counter.draw()

    @property
    def audio_volumes(self):
        """ Get audio volumes """

        return self._audio_volumes

    @property
    def root_dir(self):
        """ Root directory """
        return self._root_dir
