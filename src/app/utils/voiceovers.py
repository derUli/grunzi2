import os

import arcade

from app.utils.audiovolumes import AudioVolumes

VOICEOVER_DEFAULT = 'text00.mp3'


def voiceover_path(root_dir: str, voiceover):
    return os.path.join(root_dir, 'resources', 'speech', voiceover)


def play_voiceover(dt: float, root_dir: str, voiceover: str, audio_volumes: AudioVolumes):
    # TODO: separate volume for speech

    sound = arcade.load_sound(voiceover_path(root_dir, voiceover), streaming=audio_volumes.streaming)
    return sound.play(volume=audio_volumes.volume_sound)
