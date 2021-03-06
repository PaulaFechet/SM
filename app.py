

from flask import Flask, render_template,flash,url_for,session,request,logging,redirect
from http import cookies
import time
import os

from wtforms import Form,StringField,TextAreaField,validators

import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import math as math
import threading

GPIO.setmode(GPIO.BCM)

type = Adafruit_DHT.DHT11

dht11 = 25
GPIO.setup(dht11, GPIO.IN)


app = Flask(__name__)


def read_temp():
    # citeste temperatura de la senzor
    humidity, temperature = Adafruit_DHT.read_retry(type, dht11)
    temp = str(temperature)
    return temp

def read_umid():
    # citeste umiditatea de la senzor
    humidity, temperature = Adafruit_DHT.read_retry(type, dht11)
    umidit = str(humidity)
    return umidit


class CheForm(Form):
    email = StringField('Email',[validators.Length(min =1,max=50)])

# se primeste adresa de email de pe interfata apoi se scrie in fisier
@app.route("/",methods = ['GET','POST'])
def home_1():
    form = CheForm(request.form)
    if request.method == 'POST' and form.validate():
        mesaj = form.email.data
        printfile(mesaj)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        return redirect(url_for('home'))
    return render_template('register.html',form=form)

@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/temp",methods = ['GET','POST'])
def temp():
    temperatura = read_temp()
    if request.method == 'POST' :
        # pornire script de scriere pe diplay
        cmd = "python3 digit_temp.py"
        os.system(cmd)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
        return redirect(url_for('temp'))
    return render_template('temperatura.html',temperatura=temperatura)

@app.route("/umiditate")
def umiditate():
    # se apeleaza functia care returneaza umiditatea de a senzor apoi se trimite pe interfata pentru afisare
    umiditate = read_umid()
    return render_template('umiditate.html',umiditate=umiditate)

def printfile (mesaj):
    file = open("email.txt","w")
    file.write(mesaj)
    file.close()


@app.route("/alarma")
def alarma():
    return render_template('alarma.html')

# se primeste adresa de email de pe interfata apoi se scrie in fisier
@app.route("/register",methods = ['GET','POST'])
def register():
    form = CheForm(request.form)
    if request.method == 'POST' and form.validate():
        mesaj = form.email.data
        printfile(mesaj)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
        return redirect(url_for('home'))
    return render_template('register.html',form=form)

@app.route("/alarma-on")
def alarma_on():
    #pentru pornit alarma 
    cmd = "sudo python alarma.py"
    os.system(cmd)
    msg = "Alarma a fost pornita!"
    # se trimite mesajul de pornire alarma pe interfata
    return render_template('alarma.html',msg=msg)

@app.route("/alarma-off")
def alarma_off():
    # se opreste alarma
    msg = "Alarma a fost oprita!"
    cmd=" ps aux | grep -ie 'python alarma.py' | awk '{print $2}' | xargs sudo kill -9"
    os.system(cmd)
    # se trimite mesajul de oprire alarma pe interfata
    return render_template('alarma.html',msg=msg)

@app.route("/led")
def led():
    return render_template('led.html')

@app.route("/led-on")
def led_on():
    # Ruleaza scriptul de start led
    cmd = 'python3 start.py'
    os.system(cmd)
    msg = "Becul a fost pornit!"
    return render_template('led.html',msg=msg)

@app.route("/led-off")
def led_off():
    # Ruleaza scriptul de stop led
    cmd = 'python3 stop.py'
    os.system(cmd)
    msg = "Becul a fost oprit!"
    return render_template('led.html',msg=msg)

@app.route("/digit_temp")
def temp_digit():
	#Ruleaza scriptul de afisare temperatura
	cmd = "sudo python senzor_temp.py"
	t = threading.Thread(target=os.system, args=(cmd,))
	t.start()
	cmd = "sudo python digit_temp.py"
	t2 = threading.Thread(target=os.system, args=(cmd,))
	t2.start()
	return render_template('temperatura.html')

@app.route("/stop_display")
def stop_display():
	cmd = " ps aux | grep -ie 'python senzor_temp.py' | awk '{print $2}' | xargs sudo kill -9"
	os.system(cmd)
	cmd = " ps aux | grep -ie 'python digit_temp.py' | awk '{print $2}' | xargs sudo kill -9"
	os.system(cmd)
	return render_template("temperatura.html")

if  __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
