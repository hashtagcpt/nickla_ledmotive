# -*- coding: utf-8 -*-

# This script uses the led motive engine
###### END ######

import requests
import os
import sys
import termios
import tty
import datetime
import random
import time
from _thread import start_new_thread

brightChanged = False
abort = False
state = True
bright = 0

max_value = 4095
led_pass = '1b66c3cd5e475454'

#light_array = [350, 500, 400, 350, 550, 300, 50]
light_array = [300, 550, 400, 350, 850, 400, 85]
dark_array = [0, 0, 0, 0, 0, 0, 0]

mel_up = [100, 350, 150, 150, 450, 200, 50] #[0, 392, 0, 0, 137, 570, 0]
mel_down = [300, 500, 350, 300, 700, 300, 85] #[123, 0, 557, 0, 0, 0, 3306]

# login to ledmotive via USB connection
def login(password): # password is a string
    host = 'http://192.168.7.2:8181/api/login'
    a = requests.post(host, json={'username': 'admin', 'password': password}, verify=False)
    cookiejar = a.cookies
    return cookiejar

# get the coookiejar
cj = login(led_pass)

def set_spectrum_a(array,cookiejar): #  array is a list of integers
    host = 'http://192.168.7.2:8181/api/luminaire/1/command/SET_SPECTRUM_A'
    data = {'arg': array}
    requests.post(host,json=data,cookies = cookiejar,verify = False)

def getCh():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
        finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
        return ch

def checkKey():
        global cj
        global light_array
        global state
        global abort
        
        while True:
                c = getCh()
                if c == 'c' and not abort:
                        abort = True
                        break

start_new_thread(checkKey, ())


print ("Set to flat control\n")
                      
#get start/stop times
hourStart = 8 #9 time of day to start  
hourStopWhite = 16 # time of day to shut-off
hourStopMela = 20 # time of day to shut-off mela stim

while abort == False:
    currentTime = datetime.datetime.now().hour
    if (hourStart <= currentTime) and (currentTime < hourStopWhite):
        # set flat white stimulus
        set_spectrum_a(light_array, cj)
    elif (currentTime >= hourStopWhite) and (currentTime < hourStopMela):
        while (currentTime < hourStopMela):
              currentTime = datetime.datetime.now().hour
              set_spectrum_a(mel_up, cj)
              time.sleep(30)
              set_spectrum_a(mel_down, cj)
              time.sleep(30)
    else:
        set_spectrum_a(dark_array, cj)

print ("Aborting...")
set_spectrum_a(dark_array, cj)   
time.sleep(0.5)
