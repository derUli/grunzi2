# pylint: disable=W0223

""" The Game window """

import gettext
import logging
import os

import arcade
import pyglet

from app.constants.input.keyboard import KEY_SCREENSHOT, KEY_FULLSCREEN
from app.utils.string import label_value
from app.views.startscreen import StartScreen

_ = gettext.gettext

DRAW_RATE = 1 / 9999
UPDATE_RATE = 1 / 62
CENTER_WINDOW = True
MINIMUM_SIZE = (1280, 720)


class GameWindow(arcade.Window):
    """
    Main application class
    """

    def __init__(
            self,
            width: int,
            height: int,
            fullscreen: bool = True,
            vsync: bool = True,
    ):
        """ Constructor """

        w, h = MINIMUM_SIZE

        self._mode = None
        self._root_dir = None
        self._screen = None
        self._controller_manager = None
        self._controllers = []

        # Call the parent class and set up the window
        super().__init__(
            width=w,
            height=h,
            title=_('Welcome to Amerre'),
            fullscreen=fullscreen,
            vsync=vsync,
            resizable=True,
            draw_rate=DRAW_RATE,
            update_rate=UPDATE_RATE,
            center_window=CENTER_WINDOW
        )

    def setup(self, root_dir: str):
        """ Set up the main window here"""

        self._root_dir = root_dir

        icon = pyglet.image.load(
            os.path.join(root_dir, 'resources', 'images', 'ui', 'icon.ico')
        )
        self.set_icon(icon)
        self.setup_controllers()

        w, h = MINIMUM_SIZE
        self.set_minimum_size(w, h)
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
            logging.warning('TODO: implement screenshot')
        elif symbol in KEY_FULLSCREEN:
            logging.info(label_value('Fullscreen', not self.fullscreen))
            self.set_fullscreen(not self.fullscreen)
