# pylint: disable=W0223

""" The Game window """

import gettext
import logging
import os
import time

import arcade
import pyglet
import userpaths

from app.constants.audio import VOLUME_SOUND_FX
from app.constants.gameinfo import DIRECTORY_GAME_NAME
from app.constants.input.keyboard import KEY_SCREENSHOT
from app.constants.settings import SETTINGS_SIZE_MINIUM
from app.utils.string import label_value
from app.views.logo import Logo
from app.views.startscreen import StartScreen

_ = gettext.gettext


class GameWindow(arcade.Window):
    """
    Main application class
    """

    def __init__(
            self,
            width: int = 1280,
            height: int = 720,
            fullscreen: bool = True,
            vsync: bool = True,
            draw_rate: int = 1 / 60,
            update_rate=1 / 60,
            center_window=False,
            antialiasing: bool = True,
            samples: int = 4,
    ):
        """ Constructor """

        self._mode = None
        self._root_dir = None
        self._screen = None
        self._controller_manager = None
        self._controllers = []

        # Call the parent class and set up the window
        super().__init__(
            width=width,
            height=height,
            title=_('Welcome to Amerre'),
            fullscreen=fullscreen,
            vsync=vsync,
            resizable=False,
            draw_rate=draw_rate,
            update_rate=update_rate,
            center_window=center_window,
            antialiasing=antialiasing,
            samples=samples
        )

    def setup(self, root_dir: str, show_intro: bool = True):
        """ Set up the main window here"""

        self._root_dir = root_dir

        icon = pyglet.image.load(
            os.path.join(root_dir, 'resources', 'images', 'ui', 'icon.ico')
        )
        self.set_icon(icon)
        self.setup_controllers()

        w, h = SETTINGS_SIZE_MINIUM
        self.set_minimum_size(w, h)

        if show_intro:
            view = Logo()
        else:
            view = StartScreen()

        view.setup(root_dir)
        self.show_view(view)

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
        def on_connect(gamepad) -> None:
            """ On controller connect """
            logging.info(label_value('Controller connected', controller))

            gamepad.open()
            gamepad.push_handlers(self)

            self._controllers.append(gamepad)

        @self._controller_manager.event
        def on_disconnect(gamepad):
            """ On controller disconnect """
            logging.info(label_value('Controller disconnected', controller))
            gamepad.pop_handlers()
            gamepad.close()
            self._controllers.remove(gamepad)

    def on_button_press(self, joystick, key) -> None:
        """ On controller button pressed """

        if hasattr(self.current_view, 'on_button_press'):
            self.current_view.on_button_press(joystick, key)
        else:
            logging.error(
                label_value(
                    self.current_view.__class__.__qualname__,
                    'on_button_press not implemented'
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

    def on_screenshot(self):
        """ Save a screenshot """

        screenshot_dir = str(os.path.join(userpaths.get_my_pictures(), DIRECTORY_GAME_NAME))

        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)

        filename = os.path.join(screenshot_dir, time.strftime("%Y%m%d-%H%M%S") + '.jpg')

        start = time.time()
        image = arcade.get_image().convert('RGB')
        image.save(filename)
        end = time.time() - start

        logging.info(f"Screenshot saved as {filename} in {end} seconds")

        sound = arcade.load_sound(
            os.path.join(self._root_dir, 'resources', 'sounds', 'common', 'screenshot.mp3')
        )
        sound.play(volume=VOLUME_SOUND_FX)

        return filename
