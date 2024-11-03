""" Audio volumes """


class AudioVolumes:
    """ Audio volumes """

    def __init__(
            self,
            volume_music: float,
            volume_sound: float,
            volume_master: float,
            streaming: bool = True
    ):
        """ Constructor """

        self.volume_music = volume_music * volume_master
        self.volume_sound = volume_sound  * volume_master
        self.streaming = streaming
