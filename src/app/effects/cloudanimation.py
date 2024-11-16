
from app.constants.layers import LAYER_CLOUD


CLOUD_SPEED = 0.25

class CloudAnimation:
    def __init__(self):
        self._scence = None
        self._tilemap = None

    def setup(self, scene, tilemap):
        self._scene = scene
        self._tilemap = tilemap

    def update(self):
        clouds = self._scene[LAYER_CLOUD]

        width = self._tilemap.width * self._tilemap.tile_width

        for cloud in clouds:
            cloud.center_x -= CLOUD_SPEED

            if cloud.right <= 0:
                cloud.right = width - abs(cloud.right)
