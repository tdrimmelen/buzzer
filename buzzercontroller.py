import logging
import threading
import wave


import simpleaudio as sa


class buzzercontroller:

    def __init__(self, audiofile):
        logging.debug(self.__class__.__name__ + ": Making shotclock buzzer object")

        self.wave_read = wave.open(audiofile)
        self.audio_data = self.wave_read.readframes(self.wave_read.getnframes())


    def play(self):

         p1 = threading.Thread(target=self._play)
         p1.start()


    def _play(self):
        logging.debug(self.__class__.__name__ + ": PLAYING SHOTCLOCK BUZZER")

        i = 0
        while (i < 15):
            self.play_obj = sa.play_buffer(self.audio_data, 1, 2, 44100)
            self.play_obj.wait_done()
            i = i + 1
        logging.debug(self.__class__.__name__ + ": END OF BUZZER")
