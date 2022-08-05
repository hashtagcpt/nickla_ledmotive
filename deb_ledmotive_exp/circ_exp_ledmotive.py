#!/usr/bin/python3
# -*- coding: utf-8 -*-

# This script uses the led motive engine
###### END ######

import requests
import os
import sys
import termios
import tty
import time
import datetime as dt
import random
from _thread import start_new_thread

brightChanged = False
abort = False
state = True
bright = 0
#redSteady = True
#blueSteady = False
#greenSready = False
#whiteSteady = False
#yellowSteady = False

max_value = 4095
led_pass = '1b66c3cd5e475454'


light_array = [0, 0, 0, 0, 0, 0, 0]

mean_val = 2048

low_val = 0

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
                
                if c == 'p' and state:
                        state = False
                        print ("Pausing...")
                        
                        #light_array = [low_val,low_val,low_val,low_val,low_val,low_val]
                        #set_spectrum_a(light_array, cj)                    

                        time.sleep(10)
                        
                if c == 'w' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False
                        
                        #light_array = [mean_val,mean_val,mean_val,mean_val,mean_val,mean_val]
                        
                if c == 'c' and not abort:
                        abort = True
                        break

start_new_thread(checkKey, ())

#print("p / r = Pause / Resume\nc = Abort Program\nw = set White 4h condition\nb = set Blue 4h condition\ny = set Yellow 4h condition\n")

val = 34 # set the mean val
t = time.time()

#wonky timezone
hourStart = 9 #9 time of day to start 8h stim 
hourStop = 16 #17 # time of day to shut-off 8h stim and turn on 4h stim
stimStop = 15#21 # time of day to shut off 4h stim

while abort == False:
    currentTime = dt.datetime.now().hour  
    if currentTime >= hourStart and currentTime < stimStop:
        # set 12h light stimulus    
        light_array = [mean_val,mean_val,mean_val,mean_val,mean_val,mean_val]
        set_spectrum_a(light_array, cj)                    
    else:
        light_array = [low_val,low_val,low_val,low_val,low_val,low_val]
        set_spectrum_a(light_array, cj)                    
      
print ("Aborting...")
light_array = [low_val,low_val,low_val,low_val,low_val,low_val]
set_spectrum_a(light_array, cj)                    

t = time.time()

time.sleep(0.5)
