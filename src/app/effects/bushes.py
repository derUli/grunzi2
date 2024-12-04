import arcade

from app.constants.layers import LAYER_BUSH, LAYER_PLAYER
from app.effects.effect import Effect

FADE_SPEED = 1
ALPHA_MAX = 255
ALPHA_MIN = 255 * 0.5

MIN_DISTANCE = 64


class Bushes(Effect):

    def update(self, delta_time: float) -> None:
        """
        Update it
        @param delta_time: Float
        """

        sprites = self._scene[LAYER_BUSH]

        collides = False
        player = self._scene[LAYER_PLAYER][0]

        for sprite in sprites:
            if arcade.get_distance_between_sprites(sprite, player) < MIN_DISTANCE:
                collides = True
                break

        for sprite in sprites:
            if collides:
                sprite.alpha = max(ALPHA_MIN, sprite.alpha - FADE_SPEED)
            else:
                sprite.alpha = min(ALPHA_MAX, sprite.alpha + FADE_SPEED)
