""" Voice over trigger handling """
import logging
import os

import arcade

from app.utils.audiovolumes import AudioVolumes
from app.utils.string import label_value

VOICEOVER_DEFAULT = 'text00.mp3'


class VoiceOverTiggers:
    """ Voice over trigger handling """

    def __init__(self):
        """ Voice over trigger handling """
        self.playing = False

    def on_speech_completed(self) -> None:
        """ Executed after voice playback is completed """

        logging.info('Speech completed')
        self.playing = False

    def voiceover_path(self, root_dir: str, voiceover) -> str:
        """ Get path to voiceover """

        return os.path.join(root_dir, 'resources', 'speech', voiceover)

    def play_voiceover(
            self,
            dt: float,
            root_dir: str,
            voiceover: str,
            audio_volumes: AudioVolumes
    ):
        """ Play voiceover """

        logging.info(label_value('Speech completed', voiceover))

        sound = arcade.load_sound(
            self.voiceover_path(root_dir, voiceover),
            streaming=audio_volumes.streaming
        )

        playback = sound.play(volume=audio_volumes.volume_speech)
        playback.on_player_eos = self.on_speech_completed

        return playback
