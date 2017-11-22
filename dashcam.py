import time
import sys
import os
import picamera
import RPi.GPIO as GPIO

buttonPin = 21
dontstartpin = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(dontstartpin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
input_state = True
dontstart_state = True

dontstart_state = GPIO.input(dontstartpin)
if not dontstart_state:
	exit(0)

camera = picamera.PiCamera()

recording_time_in_minutes = 30

while input_state:
	files = os.listdir('/home/pi/dashcam_videos')
	if len(files) > 3:
		files = [os.path.join('/home/pi/dashcam_videos', f) for f in files]
		files.sort(key=lambda x: os.path.getmtime(x))
		os.system('sudo rm ' + files[0])
	camera.annotate_background = picamera.Color('black')
	camera.annotate_text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	filenametime = time.strftime("_%Y-%m-%d_%H_%M_%S", time.localtime())
	camera.start_recording('/home/pi/dashcam_videos/dashcam' + filenametime + '.h264')
	for i in range(600 * recording_time_in_minutes):
		input_state = GPIO.input(buttonPin)
		if not input_state:
			time.sleep(0.05)
			GPIO.cleanup()
			break
		camera.annotate_text = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
		camera.wait_recording(0.1)
	camera.stop_recording()
os.system('sudo shutdown -h now') #turn off pi into sleep state
