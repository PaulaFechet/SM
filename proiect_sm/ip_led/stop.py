import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

port = 21

GPIO.setwarnings(False)

GPIO.setup(port, GPIO.OUT)

GPIO.output(port, GPIO.LOW)
