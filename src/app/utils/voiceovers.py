import logging
import os

import arcade

from app.utils.audiovolumes import AudioVolumes
from app.utils.string import label_value

VOICEOVER_DEFAULT = 'text00.mp3'


def voiceover_path(root_dir: str, voiceover):
    """ Get path to voiceover """
    return os.path.join(root_dir, 'resources', 'speech', voiceover)


def play_voiceover(dt: float, root_dir: str, voiceover: str, audio_volumes: AudioVolumes, on_player_eos):
    """ Play voiceover """

    logging.info(label_value('Speech completed', voiceover))

    sound = arcade.load_sound(voiceover_path(root_dir, voiceover), streaming=audio_volumes.streaming)

    playback = sound.play(volume=audio_volumes.volume_speech)
    playback.on_player_eos = on_player_eos

    return playback
