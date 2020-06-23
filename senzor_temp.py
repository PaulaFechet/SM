import RPi.GPIO as GPIO
import Adafruit_DHT #import librarie pentru luarea de la senzor a temperaturii si a umiditatii
import time
import math as math
import threading

GPIO.setmode(GPIO.BCM)

type = Adafruit_DHT.DHT11

dht11 = 25  #conectare senor la raspberry pi, pinul 25
GPIO.setup(dht11, GPIO.IN)


def printfile (str):  #functie scriere in fisier temperatura si umiditate
        file = open("file.txt","w")
	file.write(str)
	file.close()


def readfile(): #functie citire din fisier
	file =open("file.txt","r")
	str = ''
	str += file.read()
	file.close()
	return str


def temp_print(temp): #functie scriere in fisier temperatura
	file = open("temp.txt", "w")
	file.write(temp)
	file.close()

try:

	while True:
		humidity, temperature = Adafruit_DHT.read_retry(type, dht11) #luare de la senzor a temperaturii si umiditatii
		if humidity is not None and temperature is not None:
			temp_print(str(temperature)) #scriere temperatura in fisier, de unde va fi citita pentru senzor
			buffer = ' Temperature = ' + str(temperature) + '\t' + 'Umiditate = ' + str(humidity)
			printfile(buffer) #scriere temperatura si umiditate in fisier


except KeyboardInterrupt:
	pass

GPIO.cleanup()
