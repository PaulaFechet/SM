
from flask import Flask, render_template,flash,url_for,session,request,logging,redirect
from http import cookies
import time
import os

from wtforms import Form,StringField,TextAreaField,validators

# import RPi.GPIO as GPIO
# import Adafruit_DHT
# import time
# import math as math
# import threading

# GPIO.setmode(GPIO.BCM)

# type = Adafruit_DHT.DHT11

# dht11 = 25
# GPIO.setup(dht11, GPIO.IN)


app = Flask(__name__)

def read_temp():
    # humidity, temperature = Adafruit_DHT.read_retry(type, dht11)
    # temp_print(str(temperature))
	# buffer = ' Temperature = ' + str(temperature) + '\t' + 'Umiditate = ' + str(humidity)
    return 34

def read_umid():
    # humidity, temperature = Adafruit_DHT.read_retry(type, dht11)
    # temp_print(str(temperature))
	# buffer = ' Temperature = ' + str(temperature) + '\t' + 'Umiditate = ' + str(humidity)
    return 34


class CheForm(Form):
    email = StringField('Email',[validators.Length(min =1,max=50)])

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
         

@app.route("/temperatura")
def temp():  
    temperatura = read_temp()
    return render_template('temperatura.html',temperatura=temperatura)
       
@app.route("/umiditate")
def umiditate():  
    umiditate = read_umid()
    return render_template('umiditate.html',umiditate=umiditate)
       

def printfile (mesaj):
    file = open("email.txt","w")
    file.write(mesaj)
    file.close()

@app.route("/alarma",methods = ['GET','POST'])
def alarma():  
    form = CheForm(request.form)
    if request.method == 'POST' and form.validate():
        mesaj = form.email.data
        printfile(mesaj)     
        msg = "Alarma a fost pornita!"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        return redirect(url_for('alarma',msg=msg))
    return render_template('alarma.html',form=form)


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
    return render_template('alarma.html',msg=msg)

@app.route("/alarma-off")
def alarma_off(): 
    msg = "Alarma a fost oprita!"
    cmd=" ps aux | grep -ie 'python alarma.py' | awk '{print $2}' | xargs sudo kill -9"
    os.system(cmd)
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

if  __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
