
import arcade
import pyglet

from app.views.startscreen import StartScreen

import gettext
_ = gettext.gettext


FULLSCREEN = False
VSYNC = False
DRAW_RATE = 1 / 9999
UPDATE_RATE = 1 / 62
CENTER_WINDOW = True
SCREEN_SIZE = (1366, 768)

class GameWindow(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        """ Constructor """
        w, h = SCREEN_SIZE
        self.mode = None

        if FULLSCREEN:
            screen = pyglet.canvas.get_display().get_default_screen()
            self.mode = screen.get_closest_mode(self.width, self.height)

        # Call the parent class and set up the window
        super().__init__(
            width=w,
            height=h,
            fullscreen=FULLSCREEN,
            vsync=VSYNC,
            draw_rate=DRAW_RATE,
            update_rate=UPDATE_RATE,
            center_window=CENTER_WINDOW
        )


    def setup(self):
        """ Set up the main window here"""

        if self.mode:
            """ Change screen resolution if fullscreen """
            self._set_fullscreen_mode(self.mode, self.width, self.height)

        view = StartScreen()
        view.setup()
        self.show_view(view)

    def size(self):
        return self.width, self.height

