from clockbuzzer import Clockbuzzer
import logging
import os

if __name__ == "__main__":

    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=LOGLEVEL)

    clockbuzzer = Clockbuzzer()

    clockbuzzer.run()