import os

import arcade

from app.gamewindow import GameWindow


root_dir = os.path.dirname(os.path.abspath(__file__))
window = GameWindow()
window.setup(root_dir)
arcade.run()