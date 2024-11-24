#!/usr/bin/env python3
# coding=utf-8

""" Main file """
import logging
import os
import sys

import pyglet

pyglet.options['debug_gl'] = False

if hasattr(sys, 'frozen'):
    root_dir = os.path.dirname(os.path.abspath(sys.executable))
else:
    root_dir = os.path.dirname(os.path.abspath(__file__))

from app.startup import Startup

try:
    Startup().setup(root_dir).start()
except KeyboardInterrupt as e:
    logging.debug(e)
