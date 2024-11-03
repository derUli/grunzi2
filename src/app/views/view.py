""" View """

import arcade


class View(arcade.View):
    """ View """

    def __init__(self):
        """ Constructor """

        super().__init__()

        self._root_dir = None
        self._scene = None
        self._fade_sprite = None
        self._phase = None
        self._music = None
