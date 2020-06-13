import RPi.GPIO as GPIO
import time
import smtplib
import signal
import atexit


def terminate():
#	server.quit()
#	GPIO.cleanup()
#	print("semnal terminare")
	file = open("fis.txt","w")
	file.write("cf?")

atexit.register(terminate)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("alarma.rbpi@gmail.com","Alarma123")
GPIO.setmode(GPIO.BOARD)
move=7
led=11
GPIO.setup(move, GPIO.IN)
time.sleep(0.1)
movesDetected = 0

prevDetection = time.localtime()
try:
	while 1:
		if GPIO.input(move)==1:
			movesDetected+=1
			timeDetection = time.localtime()
			minDetection = timeDetection.tm_min
			print("Detectie miscare")
			if prevDetection.tm_min > timeDetection.tm_min:
				minDetection = 60+timeDetection.tm_min
			if prevDetection.tm_mday != timeDetection.tm_mday or prevDetection.tm_hour != timeDetection.tm_hour or (minDetection-prevDetection.tm_min > 3 and movesDetected >=3) or movesDetected>6:
				movesDetected=0
				headers = ["From: alarma.rbpi@gmail.com", "Subject: Alarma a detectat miscare", "To: heghea.mihai@gmail.com", "MIME-Version: 1.0", "Content-Type: text/html"]
        			headers = "\r\n".join(headers)
				msg = "Alarma a detectat miscare pe data de "
				msg+= str(timeDetection.tm_mday)+"."
				msg+= str(timeDetection.tm_mon)+"."
				msg+= str(timeDetection.tm_year)+", la ora: "
				msg+=str(timeDetection.tm_hour)+":"
				msg+=str(timeDetection.tm_min)+":"
				msg+=str(timeDetection.tm_sec)+"."
				print(msg)
				server.sendmail("alarma.rbpi@gmail.com","heghea.mihai@gmail.com",headers+"\r\n\r\n"+ msg)
				prevDetection = timeDetection
			if minDetection-prevDetection.tm_min>3 and movesDetected<3:
				movesDetected=0
			time.sleep(4)
except Exception as excep:
	print(excep)
finally:
	GPIO.cleanup()
