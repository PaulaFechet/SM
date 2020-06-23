import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

port = 21 #alege pin 21 ca pin de iesire

GPIO.setwarnings(False)

GPIO.setup(port, GPIO.OUT) #seteaza pinul 21 ca pin de iesire

GPIO.output(port, GPIO.HIGH) #pune pinul pe HIGH pentru a aprinde becul
