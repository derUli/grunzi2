""" Game startup """
import logging
import sys

import arcade

from app.gamewindow import GameWindow


class Startup:
    """ Game startup """

    def __init__(self):
        """ Constructor """
        self.args = None
        self._root_dir = None

    def setup(self, root_dir: str):
        """ Setup game startup """

        self._root_dir = root_dir
        self.setup_logging()

    @staticmethod
    def setup_logging():
        """ Configure logger """

        handlers = [logging.StreamHandler(stream=sys.stdout)]
        log_level = logging.INFO
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=handlers
        )

    def start(self):
        """ Start game """

        window = GameWindow()
        window.setup(self._root_dir)
        arcade.run()
