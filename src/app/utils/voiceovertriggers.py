""" Voice over trigger handling """
import logging
import os
import random

import arcade

from app.utils.audiovolumes import AudioVolumes
from app.utils.string import label_value

VOICEOVER_DEFAULT = 'text00.mp3'


class VoiceOverTiggers:
    """ Voice over trigger handling """

    def __init__(self):
        """ Voice over trigger handling """
        self.playing = False
        self.randomized_voiceovers = []

    def setup(self):
        """ Setup """

        voiceovers = []

        for i in range(1, 6):
            voiceovers.append("text" + str(i).rjust(2, '0') + '.mp3')

        random.shuffle(voiceovers)

        self.randomized_voiceovers = voiceovers

        return self

    def on_speech_completed(self) -> None:
        """ Executed after voice playback is completed """

        logging.info('Speech completed')
        self.playing = False

    @staticmethod
    def voiceover_path(root_dir: str, voiceover: str) -> str:
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

        logging.info(label_value('Play speech', voiceover))

        sound = arcade.load_sound(
            self.voiceover_path(root_dir, voiceover),
            streaming=audio_volumes.streaming
        )

        playback = sound.play(volume=audio_volumes.volume_speech)
        playback.on_player_eos = self.on_speech_completed

        return playback

    def pop(self, first=False) -> str|None:
        """ Pop voiceover """

        if first:
            return VOICEOVER_DEFAULT

        if not any(self.randomized_voiceovers):
            return None
        return self.randomized_voiceovers.pop(0)
