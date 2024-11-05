""" Main file """
import logging
import os

from app.startup import Startup

root_dir = os.path.dirname(os.path.abspath(__file__))

try:
    Startup().setup(root_dir).start()
except KeyboardInterrupt as e:
    logging.debug(e)
