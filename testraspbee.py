
import RPi.GPIO as GPIO
import cgitb;


import spidev
import time
import json
cgitb.enable()
import requests


GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)


spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

def readpot(potmeter):
    if ((potmeter > 7) or (potmeter < 0)):
        return -1
    r = spi.xfer2([1, (8 + potmeter) << 4, 0])
    time.sleep(0.000005)
    potout = ((r[1] & 3) << 8) + r[2]
    return potout

def blink(pin):
	#setup GPIO output channel
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, 1)
	time.sleep(0.5)
	GPIO.output(pin, 0)
	time.sleep(0.5)




print("Aan het berekenen...")

warmte = readpot(0)
oogst = readpot(1)


try:
    while True:

        warmte = readpot(0)
        oogst = readpot(1)

        if warmte > 750!= True:
            print("WARNING - ", "Temperatuur is Te warm!", warmte , "Graden")
            warm_sended = True
            blink(17)
            time.sleep(2)

        if 200 < warmte < 750!= True:
            print("Temperatuur is Goed", warmte , "Graden")
            time.sleep(2)

        if warmte < 200!= True:
            print("Warning - ", "Temperatuur is Te koud!", warmte ,"Graden")
            time.sleep(2)

        if oogst > 500 != True:
            print("Warning - ", "Korf is Vol!")
            time.sleep(2)
        if 200 < oogst < 500!= True:
            print("Korf is Goed")

        if oogst < 200!= True:
            print("WARNING ", " Korf is Leeg")
            time.sleep(2)

        if GPIO.input(17):
            time.sleep(1)
        elif GPIO.input(17) == False:
            time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()
    client_sock.close()
    server_sock.close()
