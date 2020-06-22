import RPi.GPIO as GPIO
import time
import smtplib

def readEmail():
	f = open("email.txt", "r") # se deschide fisierul cu adresa de mail
	return f.read() # se intoarce un sir de caractere care contine adresa de mail


server = smtplib.SMTP('smtp.gmail.com', 587) #instantiere server smtp
server.starttls() #porinre server smtp
server.login("alarma.rbpi@gmail.com","Alarma123") # conectare cu adresa de mail care o sa trimita mail utilizatorului
GPIO.setmode(GPIO.BOARD) # alegerea modului de utilizare al pinilor
move=7 # pinul pe care se primeste semnalul atunci cand senzorul detecteaza miscare
GPIO.setup(move, GPIO.IN) # pinul 7 trebuie sa fie de tip input
time.sleep(0.1)
movesDetected = 0 # initial nu s-a detectat nicio miscare

prevDetection = time.localtime() # momentul detectiei miscarii anterioare atunci cand porneste aplicatia este momentul pornirii acesteia
try:
	while 1:
		if GPIO.input(move)==1: # atunci cand detecteaza miscare
			movesDetected+=1 # numarul de miscari detectate de la ultima averizare este incrementat
			timeDetection = time.localtime() # se preia momentul detectiei miscarii
			minDetection = timeDetection.tm_min 
			print("Detectie miscare")
			if prevDetection.tm_min > timeDetection.tm_min: # daca minutul detectiei este din ora urmatoare sau mai tarziu 
				minDetection = 60+timeDetection.tm_min # se aduna cu 60 (numarul de minute al unei ore) pentru a se putea face diferenta mai jos
			if prevDetection.tm_mday != timeDetection.tm_mday or prevDetection.tm_hour != timeDetection.tm_hour or (minDetection-prevDetection.tm_min > 2 and movesDetected >=2) or movesDetected>4:
				#daca se detecteaza miscare in alta zi sau alt ora sau in interval de 2 minute se inregistreaza cel putin 2 miscari sau se 
				# inregistreaza mai mult de 4 miscari in mai putin de 2 minute, este trimis mail catre utilizator cu o avertizare
				movesDetected=0 # se reseteaza numarul de miscari detectate
				headers = ["From: alarma.rbpi@gmail.com", "Subject: Alarma a detectat miscare", "To: heghea.mihai@gmail.com", "MIME-Version: 1.0", "Content-Type: text/html"]
        			headers = "\r\n".join(headers) # se construieste header-ul mail-ului
				msg = "Alarma a detectat miscare pe data de "
				msg+= str(timeDetection.tm_mday)+"."
				msg+= str(timeDetection.tm_mon)+"."
				msg+= str(timeDetection.tm_year)+", la ora: "
				msg+=str(timeDetection.tm_hour)+":"
				msg+=str(timeDetection.tm_min)+":"
				msg+=str(timeDetection.tm_sec)+"." # se construieste mesajul trimis prin mail, acesta contine data, ora, minutul si secunda la care s-a raportat acea avertizare
				print(msg)
				email = readEmail() # se preia adresa de mail catre care sa se trimita acel mail, adresa se va adauga din interfata web
				print("Mesaj trimis catre: "+email)
				server.sendmail("alarma.rbpi@gmail.com",email ,headers+"\r\n\r\n"+ msg) # trimiterea efectiva a mail-ului
				prevDetection = timeDetection # momentul detectiei anterioare devine momentul detectiei curente
			if minDetection-prevDetection.tm_min>2 and movesDetected<2:
				movesDetected=0 # in cazul in care in 2 minute nu se detecteaza cel putin 2 miscari, se reseteaza numarul de miscari si implicit si intervalul
			time.sleep(4)
except Exception as excep:
	print(excep)
finally:
	GPIO.cleanup()
