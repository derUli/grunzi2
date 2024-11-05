""" Main file """

import os

from app.startup import Startup

root_dir = os.path.dirname(os.path.abspath(__file__))
Startup().setup(root_dir).start()
