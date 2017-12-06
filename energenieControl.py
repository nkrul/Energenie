#!/usr/bin/python3

#import the required modules
import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)

# set the pins numbering mode
GPIO.setmode(GPIO.BOARD)

# Select the GPIO pins used for the encoder D0-D3 data inputs
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

# Select the signal used to select ASK/FSK
GPIO.setup(18, GPIO.OUT)

# Select the signal used to enable/disable the modulator
GPIO.setup(22, GPIO.OUT)

# Disable the modulator by setting CE pin lo
GPIO.output (22, False)

# Set the modulator to ASK for On Off Keying 
# by setting MODSEL pin lo
GPIO.output (18, False)

# Initialise D0-D3 inputs of the encoder to 0000
GPIO.output (11, False)
GPIO.output (15, False)
GPIO.output (16, False)
GPIO.output (13, False)

#standard template for sending control codes
def output(state):
	GPIO.output (11, 1 if state[3] == '1' else 0)
	GPIO.output (15, 1 if state[2] == '1' else 0)
	GPIO.output (16, 1 if state[1] == '1' else 0)
	GPIO.output (13, 1 if state[0] == '1' else 0)
	# let it settle, encoder requires this
	time.sleep(0.1)
	# Enable the modulator
	GPIO.output (22, 1)
	# keep enabled for a period
	time.sleep(0.25)
	# Disable the modulator
	GPIO.output (22, 0)

if len(sys.argv) == 3:
	state = ""
	if sys.argv[2] == "ON":
		state = "1"
	elif sys.argv[2] == "PAIR":
		state = "1"
	elif sys.argv[2] == "OFF":
		state = "0"
	else:
		raise Exception("Please use ON or OFF")

	if sys.argv[1] == "1":
		state = state + "111"
	elif sys.argv[1] == "2":
		state = state + "110"
	elif sys.argv[1] == "3":
		state = state + "101"
	elif sys.argv[1] == "4":
		state = state + "100"
	elif sys.argv[1] == "ALL":
		state = state + "011"
	else:
		raise Exception("Switches go from 1 to 4 (or 'ALL')")
	print ("sending " + state)
	output(state)

else:
	print ("usage:")
	print ("    ./energenieControl.py <n> <state>")
	print ("        n is from 1 to 4")
	print ("        state is ON or OFF")
	print ("Press and hold the switch power button for 5 seconds for pairing mode")
	print ("Hold switch for 10 seconds to reset")

GPIO.cleanup()
	
