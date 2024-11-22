import logging
import time
import traceback
import requests, requests.exceptions
import json
import buzzercontroller
import os	

class Signalbuzzer:

	def __init__(self):

		self.clockurl = os.environ['BUZZER_CLOCKURL']
		audiofile = os.environ['BUZZER_AUDIOFILE']

		logging.info('Clock URL = ' + self.clockurl)
		logging.info('Audiofile = ' + audiofile)

		self.buzzer = buzzercontroller.buzzercontroller(audiofile)
		self.buzzed = True
	
	def playWhenNeeded(self, buzz):

		if buzz and not(self.buzzed):

			#Only buzz once 
			logging.info('Play buzzer')
			self.buzzer.play()

		self.buzzed = buzz
			
	def run(self):

		while True:
			try:
				response = requests.get(self.clockurl, timeout = 5)
				if (response.status_code == 200):
					data = response.json()
					logging.debug('Receiving json: ' + response.text)
					if (data['status'] == 'OK'):

						buzzer = data.get('buzzer')
						logging.debug('Buzzer signal: ' + str(buzzer))

						self.playWhenNeeded(buzzer)

					else:
						message = data['ErrorMessage']
						detail = data['ErrorDetail']
						logging.error(message + ': ' + detail)
				else:
					logging.error('HTTP status received different from 200: ' + str(response.status_code))
			except requests.exceptions.Timeout:
					logging.error('Timeout exception raised')
					traceback.print_stack()
			except requests.exceptions.RequestException:
					logging.error('Request exception raised')
					traceback.print_stack()

			time.sleep(0.1)