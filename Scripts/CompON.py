# Requires a modified PowerSwitch in the target computer
# System below has a relay in parallel with the switch, with the relay controlled by GPIO 14
#
# Tests to see if computer is On. If(On): Do nothing; Else: Push Start Button

import os
import RPi.GPIO as GPIO
import time
import flask_config as cfg

ipaddress = cfg.pc_ipaddress
response = os.system('ping -c 1 '+ipaddress)
# 0 if on, non-zero if failed
if response == 0:
    # PC is On, do nothing
    print('Computer is already on, nothing executed')
else:
    # PC is non-responsive, turn on
    GPIO.setmode(GPIO.BCM) # uses GPIO pin order
    GPIO.setup(14, GPIO.OUT) # sets pin to use
    
    print('closing relay')
    GPIO.output(14,False) # applies power to control in relay, opening it
    time.sleep(0.25) # after time runs, relay is turned off
    
    GPIO.cleanup()
    print('opening relay')
    print('Computer did not respond, and Start Switch was actuated')


