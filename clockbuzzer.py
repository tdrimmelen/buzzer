import logging
import time
import traceback
import requests, requests.exceptions
import json
import buzzercontroller
import os

class Clockbuzzer:

	def __init__(self):

		self.clockurl = os.environ['BUZZER_CLOCKURL']
		audiofile = os.environ['BUZZER_AUDIOFILE']

		logging.info('Clock URL = ' + self.clockurl)

		self.buzzer = buzzercontroller.buzzercontroller(audiofile)
		self.hasBuzzed = True
	
	def playWhenNeeded(self, time):

		if (time == 0 and not self.hasBuzzed):

			self.buzzer.play()
			self.hasBuzzed = True
			
		if (time != 0):
	
			self.hasBuzzed = False

	def run(self):

		while True:
			try:
				response = requests.get(self.clockurl, timeout = 5)
				if (response.status_code == 200):
					data = response.json()
					logging.debug('Receiving json: ' + response.json())
					if (data['status'] == 'OK'):

						# Shotclock
						# If a time field is present, use it in the calculation
						if(data.get('time') != None):
							second = data['time']

						# Scoreboard
						# If a second field is present, use it in the calculation
						if(data.get('second') != None):
							second = data['second']

						# If a minute field is present, use it in the calculation
						if (data.get('minute')  != None):
							second = data['minute']*60 + second

						self.playWhenNeeded(second)
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