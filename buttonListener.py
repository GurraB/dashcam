import RPi.GPIO as GPIO
import time
import os
buttonPin = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

input_state = True

while True:
	input_state = GPIO.input(buttonPin)
	if not input_state:
		GPIO.cleanup()
		os.system('sudo python /home/pi/dashcamera/dashcam.py')
		break
