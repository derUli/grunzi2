#pylint: disable=W0223

""" The Game window """

import gettext
import os

import arcade
import pyglet

from app.views.startscreen import StartScreen

_ = gettext.gettext

FULLSCREEN = False
VSYNC = False
DRAW_RATE = 1 / 9999
UPDATE_RATE = 1 / 62
CENTER_WINDOW = True
MINIMUM_SIZE = (1280, 720)

class GameWindow(arcade.Window):
    """
    Main application class
    """

    def __init__(self):
        """ Constructor """

        w, h = MINIMUM_SIZE

        self._mode = None
        self._root_dir = None
        self._screen = None

        # Call the parent class and set up the window
        super().__init__(
            width=w,
            height=h,
            title=_('Welcome to Amerre'),
            fullscreen=FULLSCREEN,
            vsync=VSYNC,
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

        w, h = MINIMUM_SIZE
        self.set_minimum_size(w, h)
        view = StartScreen()
        view.setup(root_dir)
        self.show_view(view)

    @property
    def size(self):
        """ Window size """

        return self.width, self.height
