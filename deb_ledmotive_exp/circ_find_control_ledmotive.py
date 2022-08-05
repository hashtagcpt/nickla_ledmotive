# -*- coding: utf-8 -*-

# This script uses the led motive engine
###### END ######

import requests
import os
import sys
import termios
import tty
import time
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

#light_array = [350, 500, 400, 350, 550, 300, 50]
light_array = [300, 550, 400, 350, 850, 400, 85]
# low white flicker - 400 lx # light_array = [100, 350, 150, 150, 450, 200, 50]
light_array = [300, 500, 350, 300, 700, 300, 85]


# RGB values stimulus conditions - requires calibration
#yellow_RGB = [128, 128, 0] # set values for Greg/Hannah cage
#white_RGB = [128, 128, 128] #
#blue_RGB = [0, 0, 128] #

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
                
                if c == '1' and bright < max_value and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False
                        
                        for i in range(0, len(light_array)):
                            light_array[i] = light_array[i] + 1

                        #light_array[0] = light_array[0] + 1
                        bright = bright + 1
                        print ("Current brightness: %d" % bright)
                        
                if c == 'q' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False
                        
                        light_array[0] = light_array[0] - 1
                        bright = bright - 1
                        print ("Current brightness: %d" % bright)
                
                if c == '2' and bright < max_value and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False
                        
                        light_array[1] = light_array[1] + 1
                        bright = bright + 1
                        print ("Current brightness: %d" % bright)
                        
                if c == 'w' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False
                        
                        light_array[1] = light_array[1] - 1
                        bright = bright - 1
                        print ("Current brightness: %d" % bright)       


                if c == '3' and bright < max_value and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        light_array[2] = light_array[2] + 1                        
                        bright = bright + 1
                        print ("Current brightness: %d" % bright)
                        
                if c == 'e' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        light_array[2] = light_array[2] - 1                        
                        bright = bright - 1
                        print ("Current brightness: %d" % bright)

                if c == '4' and bright < max_value and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        light_array[3] = light_array[3] + 1                                                
                        bright = bright + 1
                        print ("Current brightness: %d" % bright)
                        
                if c == 'r' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False
                        
                        light_array[3] = light_array[3] - 1                        
                        bright = bright - 1
                        print ("Current brightness: %d" % bright)        

                if c == '5' and bright < max_value and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        light_array[4] = light_array[4] + 1                                                                        
                        bright = bright + 1
                        print ("Current brightness: %d" % bright)
                        
                if c == 't' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        light_array[4] = light_array[4] - 1                                                
                        bright = bright - 1
                        print ("Current brightness: %d" % bright)        

                if c == '6' and bright < max_value and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        light_array[5] = light_array[5] + 1                      
                        bright = bright + 1
                        print ("Current brightness: %d" % bright)
                        
                if c == 'y' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        light_array[5] = light_array[5] - 1                                                                        
                        bright = bright - 1
                        print ("Current brightness: %d" % bright)        

                if c == '7' and bright < max_value and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        light_array[6] = light_array[6] + 1                                              
                        bright = bright + 1
                        print ("Current brightness: %d" % bright)
                        
                if c == 'u' and bright > 0 and not brightChanged:
                        brightChanged = True
                        time.sleep(0.01)
                        brightChanged = False

                        light_array[6] = light_array[6] - 1                                                                                                
                        bright = bright - 1
                        print ("Current brightness: %d" % bright)        
                        
                if c == 'c' and not abort:
                        abort = True
                        break

start_new_thread(checkKey, ())


print ("Increase / Decrease (1--7, QWERTYU\n\nc = Abort Program\n")

val = 128 # set the mean val
t = time.time()

while abort == False:        
        set_spectrum_a(light_array, cj)                    
                      
print ("Aborting...")

time.sleep(0.5)
