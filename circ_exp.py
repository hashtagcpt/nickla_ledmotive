#!/usr/bin/python
# -*- coding: utf-8 -*-

# This script needs pigpio daemon running to work (http://abyz.co.uk/rpi/pigpio/)

###### CONFIGURE THIS ######

# The Pins on PI. Use Broadcom numbers. Depends on wiring!

RED_PIN   = 17
GREEN_PIN = 27
BLUE_PIN  = 22

import os
import sys
import termios
import tty
import pigpio
import time
import random
import datetime as dt
from thread import start_new_thread

# init values 
bright = 255 # set brightness here
r = 255.0
g = 255.0
b = 255.0

# set boolean values for conditions
brightChanged = False
abort = False
state = True
yellowSteady = False
blueSteady = True
whiteSteady = False

# DAC pin setup for PIGPIO
maxV = 255
freq = 500
pi = pigpio.pi()
pi.set_PWM_frequency(BLUE_PIN,freq)
pi.set_PWM_frequency(RED_PIN,freq)
pi.set_PWM_frequency(GREEN_PIN,freq)
pi.set_PWM_range(BLUE_PIN,maxV)
pi.set_PWM_range(RED_PIN,maxV)
pi.set_PWM_range(GREEN_PIN,maxV)

# RGB values stimulus conditions - requires calibration
yellow_RGB = [87, 87, 0] # set values for Greg cage
white_RGB = [55, 55, 55] # .649 w/sr/m2

#blue_RGB = [0, 0, 255] # 1.01 w/sr/m2 - blue 255, 120 cd/m2,Dr. 1912lx, center 88  
blue_RGB = [0, 0, 109] # watts equal - dr. meter, 600 white, 719 blue
 
# blue_RGB = [0, 0, 87] # lum equal - dr. meter, 600 lux for both
# 87 B value is .657 w/sr/m2
def setLights(pin, brightness):
	#realBrightness = int(int(brightness) * (float(bright)) / 255.0)
        realBrightness = brightness
	pi.set_PWM_dutycycle(pin, realBrightness)


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
	global bright
	global brightChanged
	global state
	global abort
	global yellowSteady
	global blueSteady
        global whiteSteady
        global yellow_RGB
        global blue_RGB
        global white_RGB

	while True:
		c = getCh()
		if c == 'p' and state:
			state = False
			print ("Pausing...")
			
			time.sleep(0.1)
			
			setLights(RED_PIN, 0)
			setLights(GREEN_PIN, 0)
			setLights(BLUE_PIN, 0)
			
		if c == 'r' and not state:
			state = True
			print ("Resuming...")

		if c == 'b':
                        blueSteady = True
                        whiteSteady = False
                        yellowSteady = False
                        print("Setting blue 4h.")

		if c == 'w':
                        yellowSteady = False
                        blueSteady = False
                        whiteSteady = True
                        print("Setting white 4h.")

                if c == 'y':
                        yellowSteady = True
                        blueSteady = False
                        whiteSteady = False
                        print("Setting yellow 4h.")

		if c == 'c' and not abort:
			abort = True
			break

start_new_thread(checkKey, ())

print("p / r = Pause / Resume\nc = Abort Program\nw = set White 4h condition\nb = set Blue 4h condition\ny = set Yellow 4h condition\n")

val = 34 # set the mean val
t = time.time()

#wonky timezone
hourStart = 9-4 #9 time of day to start 8h stim 
hourStop = 17-4 #17 # time of day to shut-off 8h stim and turn on 4h stim
stimStop = 21-4 # time of day to shut off 4h stim

while abort == False:
    currentTime = dt.datetime.now().hour        
    if hourStart <= currentTime < hourStop:
        # set 8h stimulus
        r = setLights(RED_PIN, white_RGB[0])
        g = setLights(GREEN_PIN, white_RGB[1])
        b = setLights(BLUE_PIN, white_RGB[2])        
    elif currentTime >= hourStop and currentTime < stimStop:
        # set 4h stimulus    
        if yellowSteady == True:
                r = setLights(RED_PIN, yellow_RGB[0])
                g = setLights(GREEN_PIN, yellow_RGB[1])
                b = setLights(BLUE_PIN, yellow_RGB[2])

        elif blueSteady == True:
                r = setLights(RED_PIN, blue_RGB[0])
                g = setLights(GREEN_PIN, blue_RGB[1])
                b = setLights(BLUE_PIN, blue_RGB[2])

        elif whiteSteady == True:
                r = setLights(RED_PIN, white_RGB[0])
                g = setLights(GREEN_PIN, white_RGB[1])
                b = setLights(BLUE_PIN, white_RGB[2])                               
    else:
        r = setLights(RED_PIN, 0)
        g = setLights(GREEN_PIN, 0)
        b = setLights(BLUE_PIN, 0)   
      
print ("Aborting...")

setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)

time.sleep(0.5)

pi.stop()
