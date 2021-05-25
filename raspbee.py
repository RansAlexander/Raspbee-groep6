import os
import cgitb ; cgitb.enable() 
import time
import busio
import digitalio
import board
import RPi.GPIO as GPIO
import requests
import threading
from adafruit_bus_device.spi_device import SPIDevice

# ubeac vars
# url = "ubeac url"
# uid = "ubeac uid"
ipv4 = os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]

# MPD Setup
client = MPDClient()
client.timeout = 10
client.idletimeout = None    
client.connect("localhost", 6600)
print(client.mpd_version)
client.clear()


# IO cleanup and init
GPIO.setmode(GPIO.BCM)
pins = []
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, 0)


# Initialize SPI bus
print("Initializing SPI bus")
spi_screen = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize SPI bus
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

# Initialize control pins for adc
cs0 = digitalio.DigitalInOut(board.CE0)  # chip select
adc = SPIDevice(spi, cs0, baudrate= 1000000)
 
# read SPI data 8 possible adc's (0 thru 7) 
def readadc(adcnum): 
    if ((adcnum > 7) or (adcnum < 0)): 
        return -1 
    with adc:
        r = bytearray(3)
        spi.write_readinto([1,(8+adcnum)<<4,0], r)
        time.sleep(0.000005)
        adcout = ((r[1]&3) << 8) + r[2] 
        return adcout