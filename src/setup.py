#!/usr/bin/env python3

""" cx_freeze setup file """

import os
import sys

import cx_Freeze

target_name = 'amerre'
base = None

if sys.platform == 'win32':
    target_name = 'Amerre.exe'

target = cx_Freeze.Executable(
    script="amerre.py",
    icon=os.path.join(
        os.path.dirname(__file__),
        'resources',
        'images',
        'ui',
        'icon.ico'
    ),
    base=base,
    target_name=target_name
)

OPTIMIZE = 0

if sys.platform == 'win32':
    OPTIMIZE = 1

options = {
    'build_exe': {
        # "include_msvcr": True, Not allowed to legal reasons
        'optimize': OPTIMIZE,
        'silent_level': 3,
        'includes': [
            'pyogg'
        ],
        'include_files': [
            'resources/',
            '../CREDITS.txt'
        ],
    }
}

cx_Freeze.setup(
    name='Amerre',
    options=options,
    executables=[
        target
    ]
)
