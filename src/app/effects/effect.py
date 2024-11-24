""" Effect """


class Effect:
    """ Effect """

    def __init__(self):
        """ Constructor """
        self._scene = None
        self._tilemap = None

    def setup(self, scene, tilemap):
        """ Setup animation """
        self._scene = scene
        self._tilemap = tilemap
