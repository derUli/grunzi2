""" Move clouds """

from app.constants.layers import LAYER_CLOUD
from app.effects.effect import Effect

CLOUD_SPEED = 0.25


class CloudAnimation(Effect):
    """ Move clouds """

    def update(self, delta_time: float):
        """ Update animation"""
        clouds = self._scene[LAYER_CLOUD]

        width = self._tilemap.width * self._tilemap.tile_width

        for cloud in clouds:
            cloud.center_x -= CLOUD_SPEED

            if cloud.right <= 0:
                cloud.right = width - abs(cloud.right)
