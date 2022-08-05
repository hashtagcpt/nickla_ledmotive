#!/usr/bin/python
# -*- coding: utf-8 -*-

# This script needs running pigpio (http://abyz.co.uk/rpi/pigpio/)


###### CONFIGURE THIS ######

# The Pins. Use Broadcom numbers.
#RED_PIN   = 17
#GREEN_PIN = 22
#BLUE_PIN  = 24

RED_PIN   = 27
GREEN_PIN = 22
BLUE_PIN  = 17

# Number of color changes per step (more is faster, less is slower).
# You also can use 0.X floats.
STEPS     = 1

###### END ######


import os
import sys
import termios
import tty
import pigpio
import time
import random
from _thread import start_new_thread

bright = 255
r = 255.0
g = 255.0
b = 255.0

brightChanged = False
abort = False
state = True
redSteady = True
blueSteady = False
greenSready = False
whiteSteady = False
yellowSteady = False

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
yellow_RGB = [128, 128, 0] # set values for Greg/Hannah cage
white_RGB = [128, 128, 128] #
blue_RGB = [0, 0, 128] #

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
	global redSteady
	global blueSteady
        global greenSteady
        global whiteSteady
        global yellowSteady
        global yellow_RGB
        global blue_RGB
        global white_RGB
        
	while True:
		c = getCh()
		
		if c == '+' and bright < maxV and not brightChanged:
			brightChanged = True
			time.sleep(0.01)
			brightChanged = False
			
			bright = bright + 1
			print(("Current brightness: %d" % bright))
			
		if c == '-' and bright > 0 and not brightChanged:
			brightChanged = True
			time.sleep(0.01)
			brightChanged = False
			
			bright = bright - 1
			print(("Current brightness: %d" % bright))
			

		if c == 'r':
                        redSteady = True
                        blueSteady = False
                        greenSteady = False
                        whiteSteady = False
                        print("Setting red steady.")
                if c == 'g':
                        redSteady = False
                        blueSteady = False
                        greenSteady = True
                        whiteSteady = False
                        print("Setting green steady.")       
             
		if c == 'b':
                        redSteady = False
                        blueSteady = True
                        greenSteady = False
                        whiteSteady = False
                        print("Setting blue steady.")

		if c == 'w':
                        redSteady = False
                        blueSteady = False
                        greenSteady = False
                        whiteSteady = True
                        print("Setting white steady.")

                if c == 'y':
                        redSteady = False
                        blueSteady = False
                        greenSteady = False
                        yellowSteady = True
                        whiteSteady = False
                        print("Setting yellow steady.")
                        
		if c == 'c' and not abort:
			abort = True
			break

start_new_thread(checkKey, ())


print ("+ / - = Increase / Decrease brightness\nc = Abort Program\n")

val = 128 # set the mean val
t = time.time()

while abort == False:        
        if redSteady == True:
                r = setLights(RED_PIN, bright)
                g = setLights(GREEN_PIN, 0)
                b = setLights(BLUE_PIN, 0)

        elif blueSteady == True:
                r = setLights(RED_PIN, 0)
                g = setLights(GREEN_PIN, 0)
                b = setLights(BLUE_PIN, bright)

        elif greenSteady == True:
                r = setLights(RED_PIN, 0)
                g = setLights(GREEN_PIN, bright)
                b = setLights(BLUE_PIN, 0)
        
        elif whiteSteady == True:
                r = setLights(RED_PIN, bright)
                g = setLights(GREEN_PIN, bright)
                b = setLights(BLUE_PIN, bright)
                
        elif yellowSteady == True:
                r = setLights(RED_PIN, bright)
                g = setLights(GREEN_PIN, bright)
                b = setLights(BLUE_PIN, 0)
                
                      
print ("Aborting...")

setLights(RED_PIN, 0)
setLights(GREEN_PIN, 0)
setLights(BLUE_PIN, 0)

time.sleep(0.5)

pi.stop()
