""" Move clouds """

from app.constants.layers import LAYER_CLOUD
from app.effects.effect import Effect

CLOUD_SPEED = 0.25


class CloudAnimation(Effect):
    """ Move clouds """

    def __init__(self):
        """ Constructor """
        self._scene = None
        self._tilemap = None

    def setup(self, scene, tilemap):
        """ Setup animation """
        self._scene = scene
        self._tilemap = tilemap

    def update(self):
        """ Update animation"""
        clouds = self._scene[LAYER_CLOUD]

        width = self._tilemap.width * self._tilemap.tile_width

        for cloud in clouds:
            cloud.center_x -= CLOUD_SPEED

            if cloud.right <= 0:
                cloud.right = width - abs(cloud.right)
