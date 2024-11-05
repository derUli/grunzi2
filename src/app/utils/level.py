""" Level """

import logging
import os

import arcade
import pyglet
from arcade import FACE_RIGHT, FACE_LEFT

from app.constants.layers import (
    LAYER_PLAYER,
    LAYER_WALL,
    LAYER_CLOUD,
    LAYERS_VOICEOVER,
    LAYER_FIRST_VOICEOVER
)
from app.utils.audiovolumes import AudioVolumes
from app.utils.voiceovertriggers import VoiceOverTiggers

VIEWPORT_BASE_H = 1440
PLAYER_MOVE_SPEED = 4
PLAYER_JUMP_SPEED = 16
PLAYER_MOVE_ANGLE = 2

MODIFIER_WALK = 1.0
MODIFIER_SPRINT = 1.4
MODIFIER_SPEECH = 1.0

GRAVITY_SLOWMO = 0.002
GRAVITY_DEFAULT = 1

ALPHA_SPEED = 1
ALPHA_MAX = 255

CLOUD_SPEED = 0.25

LIGHT_LAUNCHING_MOVEMENT_SPEED = 10
LIGHT_LAUNCHING_ROTATING_SPEED = 5
LIGHT_COLLISION_CHECK_THRESHOLD = 100


class Level:
    """ Level """

    def __init__(self):
        """ Constructor"""

        self._scene = None
        self.tilemap = None
        self._camera = None
        self._physics_engine = None
        self._can_walk = False
        self._launching_sprite = None
        self._voiceover_triggers = None
        self._music = None
        self._atmo = None

    def setup(self, root_dir: str, map_name: str, audio_volumes: AudioVolumes):
        """ Setup level """

        path = os.path.join(root_dir, 'resources', 'maps', f"{map_name}.tmx")

        self.load_tilemap(path)

        self._camera = arcade.camera.Camera2D()

        self.setup_physics_engine()
        self.wait_for_begin()

        # TODO: play music by map triggers
        music_file = os.path.join(root_dir, 'resources', 'music', 'BeforeDawn.mp3')
        music = arcade.load_sound(music_file, streaming=audio_volumes.streaming)
        self._music = music.play(volume=audio_volumes.volume_music)

        atmo_file = os.path.join(root_dir, 'resources', 'sounds', 'atmos', f"{map_name}.mp3")
        atmo = arcade.load_sound(atmo_file, streaming=audio_volumes.streaming)
        self._atmo = atmo.play(volume=audio_volumes.volume_sound, loop=True)

        self._voiceover_triggers = VoiceOverTiggers().setup()
        self.scroll_to_player()

    def setup_physics_engine(self):
        """ Setup physics engine """

        self._physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            ladders=None,
            walls=self._scene[LAYER_WALL],
            gravity_constant=GRAVITY_SLOWMO
        )

    def load_tilemap(self, path):
        """ Load tilemap """

        w, h = arcade.get_window().get_size()
        zoom = h / VIEWPORT_BASE_H

        self.tilemap = arcade.load_tilemap(path, scaling=zoom)
        self._scene = arcade.Scene.from_tilemap(self.tilemap)
        self.player.alpha = 0
        self._music = None

    def update(
            self,
            delta_time: float,
            window,
            move_horizontal: int = None,
            jump: bool = False,
            sprint: bool = False
    ):
        """ Update """

        if jump:
            self.jump()

        if move_horizontal == FACE_RIGHT:
            self.move_right(sprint)
        elif move_horizontal == FACE_LEFT:
            self.move_left(sprint)
        else:
            self.move_stop()

        self.player.alpha = min(self.player.alpha + ALPHA_SPEED, 255)
        self.scroll_to_player()

        self.update_clouds()
        self._scene.update(delta_time)
        self._scene.update_animation(delta_time)
        self.check_collision_lights(window.root_dir, window.audio_volumes)
        self.update_collision_light()

        if self._music and not self._music.playing:
            self._music.delete()

    def update_fixed(self):
        """ On Fixed update """

        self._physics_engine.update()

    def scroll_to_player(self, camera_speed=1):
        """ Scroll the window to the player. """

        player = self.player

        x, y = player.position

        self._camera.position = arcade.math.lerp_2d(
            self._camera.position, (x, y), camera_speed
        )

    def draw(self):
        """ Draw level """

        self._camera.use()
        self._scene.draw()

    def move_left(self, sprint: bool = False):
        """ Move left """

        if not self._can_walk:
            return

        modifier = MODIFIER_WALK

        if sprint:
            modifier = MODIFIER_SPRINT

        if self._voiceover_triggers.playing:
            modifier = MODIFIER_SPEECH

        self.player.change_x = -PLAYER_MOVE_SPEED * modifier
        self.player.angle -= PLAYER_MOVE_ANGLE * modifier

        if self.player.angle <= 0:
            self.player.angle = 360 - abs(self.player.angle)

    def move_right(self, sprint: bool = False):
        """ Move right """

        if not self._can_walk:
            return

        modifier = MODIFIER_WALK

        if sprint:
            modifier = MODIFIER_SPRINT

        if self._voiceover_triggers.playing:
            modifier = MODIFIER_SPEECH

        self.player.change_x = PLAYER_MOVE_SPEED * modifier
        self.player.angle += PLAYER_MOVE_ANGLE * modifier

        if self.player.angle > 360:
            self.player.angle = self.player.angle - 360

    def move_stop(self):
        """ Stop walking """

        if not self._can_walk:
            return

        self.player.change_x = 0

    def jump(self):
        """ Do jump """

        if not self._physics_engine.can_jump(y_distance=5):
            return

        speed = PLAYER_JUMP_SPEED

        if self._voiceover_triggers.playing:
            speed *= MODIFIER_SPEECH

        self._physics_engine.jump(speed)

    @property
    def player(self):
        """ The player sprite """

        return self._scene[LAYER_PLAYER][0]

    def wait_for_begin(self, dt: float = 0.0):
        """ Wait for begin of level """

        if self._physics_engine.can_jump():
            self._can_walk = True
            self._physics_engine.gravity_constant = GRAVITY_DEFAULT
            return

        pyglet.clock.schedule_once(self.wait_for_begin, 1 / 4)

    def update_clouds(self):
        """ Move the clouds """

        clouds = self._scene[LAYER_CLOUD]

        width = self.tilemap.width * self.tilemap.tile_width

        for cloud in clouds:
            cloud.center_x -= CLOUD_SPEED

            if cloud.right <= 0:
                cloud.right = width - abs(cloud.right)

    def check_collision_lights(self, root_dir: str, volumes: AudioVolumes):
        """ Check for collisions with lights """

        if self._launching_sprite or self._voiceover_triggers.playing:
            return

        found = None

        for layer in LAYERS_VOICEOVER:
            if layer in self._scene:
                for sprite in self._scene[layer]:
                    if arcade.get_distance_between_sprites(
                            self.player,
                            sprite
                    ) < LIGHT_COLLISION_CHECK_THRESHOLD:
                        logging.info(f'Collided with {layer}')
                        self._launching_sprite = sprite
                        found = layer
                        break

        if not found:
            return

        arcade.load_sound(
            os.path.join(root_dir, 'resources', 'sounds', 'lights', 'missle-launch-001.mp3'),
            streaming=volumes.streaming
        ).play(volume=volumes.volume_sound)

        self._voiceover_triggers.playing = True

        voiceover = self._voiceover_triggers.pop(
            first=found == LAYER_FIRST_VOICEOVER
        )

        pyglet.clock.schedule_once(
            self._voiceover_triggers.play_voiceover,
            2,
            root_dir,
            voiceover,
            volumes
        )

    def update_collision_light(self):
        """ Update voiceover light """

        if not self._launching_sprite:
            return

        self._launching_sprite.center_y += LIGHT_LAUNCHING_MOVEMENT_SPEED
        self._launching_sprite.angle = min(
            self._launching_sprite.angle + LIGHT_LAUNCHING_ROTATING_SPEED,
            360
        )

        if self._launching_sprite.angle >= 360:
            self._launching_sprite.angle = 0

        map_height = self.tilemap.height * self.tilemap.tile_height

        if self._launching_sprite.bottom > map_height:
            self._launching_sprite.remove_from_sprite_lists()
            self._launching_sprite = None
