""" Game startup """
import argparse
import logging
import platform
import sys

import arcade
import psutil
import pyglet
from attr.converters import optional

from app.constants.settings import (
    SETTINGS_DEFAULT_FULLSCREEN,
    SETTINGS_DEFAULT_VSYNC,
    SETTINGS_DEFAULT_SIZE,
    SETTINGS_ANTIALIASING_CHOICES,
    SETTINGS_DEFAULT_ANTIALIASING, SETTINGS_DEFAULT_DRAW_RATE, SETTINGS_DEFAULT_UPDATE_RATE
)
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

        super().__init__()

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
        vsync = SETTINGS_DEFAULT_VSYNC

        args = self.get_args()
        logging.info(args)

        if args.fullscreen:
            fullscreen = True
        elif args.window:
            fullscreen = False

        if args.vsync:
            vsync = True
        elif args.no_vsync:
            vsync = False

        show_intro = True

        if args.intro:
            show_intro = True
        elif args.no_intro:
            show_intro = False

        size = args.size
        size = size.lower()
        width, height = size.split('x')

        try:
            width, height = int(width), int(height)
        except ValueError:
            logging.error('size has invalid format')
            return

        if width == 0 or height == 0:
            logging.error('Width and height must be greater than 0')
            return

        samples = args.antialiasing
        antialiasing = samples > 0

        # Draw rate
        draw_rate = 1 / 9999

        if args.draw_rate > 0:
            draw_rate = 1 / args.draw_rate

        # Update rate

        update_rate = 1 / 62

        if args.update_rate > 0:
            update_rate = 1 / args.update_rate

        window = GameWindow(
            fullscreen=fullscreen,
            vsync=vsync,
            width=width,
            height=height,
            antialiasing=antialiasing,
            samples=samples,
            center_window=args.center_window,
            draw_rate=draw_rate,
            update_rate=update_rate,
            visible=False
        )

        # Set window location based on arguments
        x, y = window.get_location()

        if args.x is not None:
            x = args.x

        if args.y is not None:
            y = args.y

        window.set_location(x, y)
        window.set_visible(True)

        self.log_hardware_info(window)
        window.setup(self._root_dir, show_intro=show_intro)
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
            '--center-window',
            action='store_true',
            default=False,
            help='Center window on screen'
        )

        parser.add_argument(
            '--fullscreen',
            action='store_true',
            default=False,
            help='Run in fullscreen mode'
        )

        parser.add_argument(
            '--vsync',
            action='store_true',
            default=False,
            help='Enable VSync'
        )

        parser.add_argument(
            '--no-vsync',
            action='store_true',
            default=False,
            help='Disable VSync'
        )

        parser.add_argument(
            '--size',
            action='store',
            default=SETTINGS_DEFAULT_SIZE,
            help='Size of window'
        )

        parser.add_argument(
            '--intro',
            action='store_true',
            default=False,
            help='Show intro'
        )

        parser.add_argument(
            '--no-intro',
            action='store_true',
            default=False,
            help='Don\'t show intro'
        )

        parser.add_argument(
            '--draw-rate',
            action='store',
            type=int,
            help='The draw rate',
            default=SETTINGS_DEFAULT_DRAW_RATE
        )

        parser.add_argument(
            '--update-rate',
            action='store',
            type=int,
            help='The update rate',
            default=SETTINGS_DEFAULT_UPDATE_RATE
        )

        parser.add_argument(
            '--antialiasing',
            action='store',
            type=int,
            help='The antialiasing level',
            choices=SETTINGS_ANTIALIASING_CHOICES,
            default=SETTINGS_DEFAULT_ANTIALIASING
        )

        parser.add_argument(
            '-x',
            action='store',
            type=int,
            required=False,
            help = 'The X position of the window'
        )

        parser.add_argument(
            '-y',
            action='store',
            type=int,
            required=False,
            help = 'The X position of the window'
        )

        return parser.parse_args()
