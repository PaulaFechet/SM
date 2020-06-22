import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import math as math

GPIO.setmode(GPIO.BCM)
dataPin = 18
latchPin = 15
clockPin = 14

GPIO.setup(dataPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT)
GPIO.setup(clockPin, GPIO.OUT)

GPIO.output(dataPin, GPIO.LOW)
GPIO.output(latchPin, GPIO.LOW)
GPIO.output(clockPin, GPIO.LOW)

g = 0b01000000
dot = 0b10000000
zero = 191 #0b10111111
zero_no_dot = 63 #0b00111111
one = 134 #0b10000110
one_no_dot = 6 #0b00000110
two = 219 #0b11011011
two_no_dot = 91 #0b01011011
three = 207 #0b11001111
three_no_dot = 79 #0b01001111
four = 230 #0b11100110
four_no_dot = 102 #0b01100110
five = 237 #0b11101101
five_no_dot = 109 #0b01101101
six = 253 #0b11111101
six_no_dot = 125 #0b01111101
seven = 135 #0b10000111
seven_no_dot = 7 #0b00000111
eight = 255 #0b11111111
eight_no_dot = 127 #0b01111111
nine = 239 #0b11101111
nine_no_dot = 111  #0b01101111

digit = 0

def Digit(x):
	global digit
	if x == 1:
		digit = 14 #0b00001110 activeaza primul digit punand pe 0 catodul corespunzator acestuia 
	elif x == 2:
        	digit = 13 #0b00001101
	elif x == 3:
		digit = 11 #0b00001011
	elif x == 4:
		digit = 7 #0b00000111
	elif x == 5:
        	digit = 0 #0b00000000


def shift(buffer):

	global digit

	for i in range(0,8):
		GPIO.output(dataPin, (128 & (digit << i)))
		GPIO.output(clockPin, GPIO.HIGH)
		time.sleep(0.001)
        	GPIO.output(clockPin, GPIO.LOW)

	for i in range(0,8):
		GPIO.output(dataPin, (128 & (buffer << i)))
		GPIO.output(clockPin, GPIO.HIGH) 
		time.sleep(0.001)
        	GPIO.output(clockPin, GPIO.LOW)

	GPIO.output(latchPin, GPIO.HIGH)
	time.sleep(0.001)
    	GPIO.output(latchPin, GPIO.LOW)

def afla_nr(x):
	nr = 0
	global zero_no_dot
	global one_no_dot
	global two_no_dot
	global three_no_dot
	global four_no_dot
	global five_no_dot
	global six_no_dot
	global seven_no_dot
	global eight_no_dot
	global nine_no_dot
	if x == 0:
		nr = zero_no_dot
	elif x == 1:
		nr = one_no_dot
	elif x == 2:
		nr = two_no_dot
	elif x == 3:
		nr = three_no_dot
	elif x == 4:
		nr = four_no_dot
	elif x == 5:
		nr = five_no_dot
	elif x == 6:
		nr = six_no_dot
	elif x == 7:
		nr = seven_no_dot
	elif x == 8:
		nr = eight_no_dot
	elif x == 9:
		nr = nine_no_dot
	return nr


def display(temperature):
	x = math.floor((temperature *10) /100)
	a = afla_nr(x)
	y = ((temperature * 10) / 10) % 10
	b = afla_nr(y)
	z = (temperature * 10) % 10
	c = afla_nr(z)
	i = 1000

	i = 50
	while i>0:
		i = i-1
		if temperature < 0:
			Digit(1)
			shift(g)
			time.sleep(0.0000001)
		Digit(2)
		shift(a)
		time.sleep(0.0000001)
		Digit(3)
		shift(b)
		time.sleep(0.0000001)
		shift(dot)
		time.sleep(0.0000001)
		Digit(4)
		shift(c)
		time.sleep(0.0000001)
		
	
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
		file = open("temp.txt", "r")
		temp = ''
		temp +=file.read()
		temperature = float(temp)
		display(temperature)
		file.close()
except KeyboardInterrupt:
	pass

GPIO.cleanup()