""" Audio volumes """


class AudioVolumes:
    """ Audio volumes """

    def __init__(self, volume_music: float, volume_sound: float, streaming: bool = True):
        """ Constructor """

        self.volume_music = volume_music
        self.volume_sound = volume_sound
        self.streaming = streaming
