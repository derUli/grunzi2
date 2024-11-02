import arcade

FULLSCREEN = True
VSYNC = True
DRAW_RATE = 1 / 9999
UPDATE_RATE = 60

SCREEN_SIZE = (1366, 768)

class GameWindow(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        w, h = SCREEN_SIZE
        # Call the parent class and set up the window
        super().__init__(
            width=w,
            height=h,
            fullscreen=FULLSCREEN,
            vsync=VSYNC,
            draw_rate=DRAW_RATE,
            update_rate=UPDATE_RATE
        )

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        pass

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Code to draw the screen goes here


    def size(self):
        return self.width, self.height