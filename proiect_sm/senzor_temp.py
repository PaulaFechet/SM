import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import math as math
import threading

GPIO.setmode(GPIO.BCM)

type = Adafruit_DHT.DHT11

dht11 = 25
GPIO.setup(dht11, GPIO.IN)


def printfile (str):
        file = open("file.txt","w")
	file.write(str)
	file.close()


def readfile():
	file =open("file.txt","r")
	str = ''
	str += file.read()
	file.close()
	return str


def temp_print(temp):
	file = open("temp.txt", "w")
	file.write(temp)
	file.close()

try:

	while True:
		humidity, temperature = Adafruit_DHT.read_retry(type, dht11)
		if humidity is not None and temperature is not None:
			temp_print(str(temperature))
			buffer = ' Temperature = ' + str(temperature) + '\t' + 'Umiditate = ' + str(humidity)
			printfile(buffer)
			returnat = ''
			returnat += readfile()
			print(returnat)


except KeyboardInterrupt:
	pass

GPIO.cleanup()
