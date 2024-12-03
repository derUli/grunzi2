""" Effect """


class Effect:
    """ Effect """

    def __init__(self):
        """ Constructor """
        self._scene = None
        self._tilemap = None
        self._root_dir = None

    def setup(self, scene, tilemap, root_dir):
        """ Setup animation """

        self._scene = scene
        self._tilemap = tilemap
        self._root_dir = root_dir

    def update(self, delta_time):
        pass

    def draw(self):
        pass