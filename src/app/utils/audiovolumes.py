""" Audio volumes """


class AudioVolumes:
    """ Audio volumes """

    def __init__(
            self,
            volume_music: int,
            volume_sound: int,
            volume_master: int,
            volume_speech: int,
            streaming: bool = True
    ):
        """ Constructor """

        self._volume_music = volume_music
        self._volume_sound = volume_sound
        self._volume_speech = volume_speech
        self._volume_master = volume_master

        self.streaming = streaming

    @property
    def volume_master(self) -> float:
        """ Master volume converted to float """

        if self._volume_master <= 0:
            return 0.0

        return self._volume_master / 100

    @property
    def volume_music(self) -> float:
        """ Music volume converted to float """

        if self._volume_music <= 0:
            return 0.0

        return self._volume_music / 100 * self.volume_master

    @property
    def volume_sound(self) -> float:
        """ Sound volume converted to float """

        if self._volume_sound <= 0:
            return 0.0

        return self._volume_sound / 100 * self.volume_master

    @property
    def volume_speech(self) -> float:
        """ Speech volume converted to float """

        if self._volume_speech <= 0:
            return 0.0

        return self._volume_speech / 100 * self.volume_master
