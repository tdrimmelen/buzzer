from clockbuzzer import Clockbuzzer
from signalbuzzer import Signalbuzzer
import logging
import os

if __name__ == "__main__":

    LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=LOGLEVEL)

    clockurl = os.environ['BUZZER_CLOCKURL']

    if 'buzzer' in clockurl:
        buzzer = Signalbuzzer()
    else:
        buzzer = Clockbuzzer()

    buzzer.run()