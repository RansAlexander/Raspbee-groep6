from flask import Flask, render_template, url_for, request, redirect, make_response
from random import random
import threading
import requests
import RPi.GPIO as GPIO
import cgitb
import spidev
import time
from time import sleep
#import pushbullet
#from pushbullet import Pushbullet
import json
import random
url = "http://orientationproject2.hub.ubeac.io/Raspbee"
uid = "raspbee"
cgitb.enable()


GPIO.setwarnings(False)

GPIO.cleanup()
GPIO.setwarnings(False)


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)

app = Flask(__name__)

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

#pb = Pushbullet("o.3ACNnvFshIEf0BVAIXpR3hX1BX6jJH4z")
#print(pb.devices)
#dev = pb.get_device('OnePlus 3T')




def readpot(potmeter):
    if ((potmeter > 7) or (potmeter < 0)):
        return -1
    r = spi.xfer2([1, (8 + potmeter) << 4, 0])
    time.sleep(0.000005)
    potout = ((r[1] & 3) << 8) + r[2]
    return potout

def blink(pin): #licht signaal als temp koud is
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 1)
	time.sleep(0.2)
	GPIO.output(pin, 0)
	time.sleep(0.2)
	
def sos(pin): #sos signaal als temp te warm is
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 1)
	time.sleep(0.5)
	GPIO.output(pin, 0)
	time.sleep(0.5)
	GPIO.output(pin, 1)
	time.sleep(1.5)
	GPIO.output(pin, 0)
	time.sleep(0.5)
	GPIO.output(pin, 1)
	time.sleep(0.5)
	GPIO.output(pin, 0)
	time.sleep(1.0)

print("Aan het berekenen...")

warmte = readpot(0)
oogst = readpot(1)


@app.route('/', methods=["GET", "POST"])
def main():
    status = request.args.get('status')
    if status == "on":
        GPIO.output(2, GPIO.HIGH)
    elif status == "off":
        GPIO.output(2, GPIO.LOW)
    return render_template('index.html')



@app.route('/data', methods=["GET", "POST"])
def data():
    temperature = readpot(0)
    weight = readpot(1)
    data = [time.time() * 1000, temperature, weight]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

def thread_webapp():
    if __name__ == '__main__':
        app.run(debug=False, host='192.168.137.2')


def thread_main():
    try:
        while True:       
            warmte = readpot(0)
            oogst = readpot(1)

            if warmte > 750 != True:
                print("WARNING - ", "Temperatuur is Te warm!", warmte, "Graden")
                sos(17)
                sos(18)
                time.sleep(2)
#                push = dev.push_note("Opgelet!","De temperatuur is te hoog!")
            if 200 < warmte < 750 != True:
                print("Temperatuur is Goed", warmte, "Graden")
                time.sleep(2)

            if warmte < 200 != True:
                print("Warning - ", "Temperatuur is Te koud!", warmte, "Graden")
#                push = dev.push_note("Opgelet!","De temperatuur is te laag!")
                blink(17)
                time.sleep(2)

            if oogst > 500 != True:
                print("Warning - ", "Korf is Vol!")
#                push = dev.push_note("Opgelet!","De korf is vol!")
                time.sleep(2)
            if 200 < oogst < 500 != True:
                print("Korf is Goed")

            if oogst < 200 != True:
                print("WARNING ", " Korf is Leeg")
#                push = dev.push_note("Opgelet!","De korf is leeg!")
                time.sleep(2)

            if GPIO.input(17):
                time.sleep(1)
            elif GPIO.input(17) == False:
                time.sleep(1)
                
    except KeyboardInterrupt:
        GPIO.cleanup()
        
def thread_ubeac():
    while True:
        data1= {
            "id": "raspbee",
            "sensors": [{
                "id": "adc kanaal0",
                "data": readpot(0)
            }]
        }
        requests.post(url, verify=False, json=data1)
        print("sending data 1:", readpot(0))
        time.sleep(1)
        
        data2= {
            "id": "raspbee",
            "sensors": [{
                "id": "adc kanaal1",
                "data": readpot(1)
            }]
        }
    
        
        requests.post(url, verify=False, json=data2)
        print("sending data 2:", readpot(1))
        time.sleep(1)

        


t1 = threading.Thread(target=thread_main)
t2 = threading.Thread(target=thread_webapp)
t3 = threading.Thread(target=thread_ubeac)
t1.start()
t2.start()
t3.start()
