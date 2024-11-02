""" Game startup """
import argparse
import logging
import platform
import sys
import arcade
import psutil
import pyglet

from app.constants.settings import SETTINGS_DEFAULT_FULLSCREEN
from app.gamewindow import GameWindow
from app.utils.string import label_value

# pylint: disable=C0103:

try:
    import sounddevice
except OSError:
    sounddevice = None
except ImportError:
    sounddevice = None



class Startup:
    """ Game startup """

    def __init__(self):
        """ Constructor """
        self.args = None
        self._root_dir = None
        self.args = None

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

    @staticmethod
    def log_hardware_info(window: arcade.Window) -> None:
        """
        Log hardware info
        """

        # Log OS info
        uname = platform.uname()
        logging.info(label_value('OS', f"{uname.system} {uname.version}"))

        # Log CPU model
        logging.info(label_value('CPU', uname.processor))

        # Log the ram size
        ram_size = round(psutil.virtual_memory().total / 1024 / 1024 / 1024)
        logging.info(label_value('RAM', f"{ram_size} GB"))

        # Renderer is the GPU
        logging.info(label_value('GPU VENDOR', window.ctx.info.VENDOR))
        logging.info(label_value('GPU RENDERER', window.ctx.info.RENDERER))
        logging.info(label_value('GPU MAX_TEXTURE_SIZE', window.ctx.info.MAX_TEXTURE_SIZE))

        logging.info(label_value('OpenGL version', pyglet.gl.gl_info.get_version_string()))

        if not sounddevice:
            logging.info(label_value('Audio', 'Unknown'))
            return

        # Log the audio devices
        for audio in sounddevice.query_devices():
            logging.info(label_value('Audio', audio['name']))

    def start(self) -> None:
        """ Start game """

        fullscreen = SETTINGS_DEFAULT_FULLSCREEN

        args = self.get_args()

        if args.fullscreen:
            fullscreen = True
        elif args.window:
            fullscreen = False

        window = GameWindow(fullscreen)
        self.log_hardware_info(window)
        window.setup(self._root_dir)
        arcade.run()

    @staticmethod
    def get_args() -> argparse.Namespace:
        """ Get args """

        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--window',
            action='store_true',
            default=False,
            help='Run in windowed mode'
        )

        parser.add_argument(
            '--fullscreen',
            action='store_true',
            default=False,
            help='Run in fullscreen mode'
        )

        return parser.parse_args()
