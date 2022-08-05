#!/usr/bin/python
# -*- coding: utf-8 -*-

# This script needs running pigpio (http://abyz.co.uk/rpi/pigpio/)


###### CONFIGURE THIS ######

# The Pins. Use Broadcom numbers.
#RED_PIN   = 17
#GREEN_PIN = 22
#BLUE_PIN  = 24

RED_PIN   = 22
GREEN_PIN = 17
BLUE_PIN  = 24

# Number of color changes per step (more is faster, less is slower).
# You also can use 0.X floats.
STEPS     = 1

###### END ######
import requests
import os
import sys
import termios
import tty
import time
import random
from thread import start_new_thread
import pandas as pd
import numpy as np
from pr import PR655

bright = 255
r = 255.0
g = 255.0
b = 255.0

abort = False

max_value = 4095
led_pass = '1b66c3cd5e475454'

#light_array[0] = light_array[0] + 1

which_led = 0 # 0 -- 6 for the 7 sources
light_array = [0, 0, 0, 0, 0, 0, 0]
light_array[which_led] = 4095

port = '/dev/ttyACM0'
#port = '/dev/ttyACM1'

pr670 = PR655(port)

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
        global bright
        global brightChanged
        global state
        global abort
        
        while True:
                c = getCh()
                
                if c == '+' and bright < max_value and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False
                        
                        light_array[which_led] = light_array[which_led] + 1
                        bright = bright + 1
                        print ("Current brightness: %d" % bright)
                        
                if c == '-' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False
                        
                        bright = bright - 1
                        print ("Current brightness: %d" % bright)
                        

                # trigger pr670 measure        
                if c == 'm':
                        lum = pr670.getLum()
                        nm, power = pr670.getSpectrum()
                        to_write_lum = pd.DataFrame(np.array([bright,lum]))
                        to_write = pd.DataFrame(np.transpose(np.array([nm,power])))
                        #print(to_write_lum)
                        #print(to_write)
                        # write values to a file
                        file_name_lum = 'lum_' + str(which_led) + '_' + str(bright) + '.' + 'csv'
                        file_name_spect = 'spect_' + str(which_led) + '_' + str(bright) + '.' + 'csv'
                        to_write_lum.to_csv(file_name_lum, sep=',')
                        to_write.to_csv(file_name_spect, sep=',')
                        
                if c == 'c' and not abort:
                        abort = True
                        break

start_new_thread(checkKey, ())


print ("+ / - = Increase / Decrease brightness\nc = Abort Program\n")

val = 128 # set the mean val
t = time.time()

while abort == False:        
        set_spectrum_a(light_array, cj)                    
                
                      
print ("Aborting...")

time.sleep(0.5)

