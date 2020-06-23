import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

port = 21 #alehe pinul 21 ca pin de iesire

GPIO.setwarnings(False)

GPIO.setup(port, GPIO.OUT) #seteaza pinul 21 ca pin de iesire

GPIO.output(port, GPIO.LOW) #pune pinul pe LOW pentru a singe becul
