import logging
import time
import traceback
import requests, requests.exceptions
import json
import buzzercontroller
import os
from enum import Enum, auto
from datetime import datetime, timedelta

class State(Enum):
	RUNNING = auto()
	WAITING = auto()
	BUZZED = auto()
	

class Clockbuzzer:

	def __init__(self):

		self.clockurl = os.environ['BUZZER_CLOCKURL']
		offset = os.environ.get('BUZZER_OFFSET', 0.0)
		audiofile = os.environ['BUZZER_AUDIOFILE']

		logging.info('Clock URL = ' + self.clockurl)
		logging.info('Buzzer offset = ' + str(offset))
		logging.info('Audiofile = ' + audiofile)

		self.buzzer = buzzercontroller.buzzercontroller(audiofile)
		self.offset = timedelta(seconds=offset)
		self.buzzertime = 0
		self.state = State.BUZZED
	
	def playWhenNeeded(self, time):

		if self.state is State.RUNNING:

			if time == 0:
				self.buzzertime = datetime.now() + self.offset
				self.state = State.WAITING

		elif self.state is State.WAITING:

			time = datetime.now()
			if (time > self.buzzertime):
				self.buzzer.play()
				self.state = State.BUZZED

		else:
			pass
			
		if (time != 0):
	
			self.state = State.RUNNING

	def run(self):

		while True:
			try:
				response = requests.get(self.clockurl, timeout = 5)
				if (response.status_code == 200):
					data = response.json()
					logging.debug('Receiving json: ' + response.text)
					if (data['status'] == 'OK'):

						second = 0

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

						logging.debug('Time in seconds: ' + str(second))
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