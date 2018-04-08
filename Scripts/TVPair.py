# Uses pyvizio api to pair with TV
# TV will sometimes invalidate your authentication (unsure if time based or TV was updated)
#
# API Source Link: https://github.com/vkorn/pyvizio
#
# I spent more time then it was worth trying to create a specific script to run
# the power on/off command. It ended up being easier just to run the command
# using 'os.system'

import os
import flask_config as cfg

# Using pyvizio send this command in terminal:
# IP is known, no need for discovery
# Pair, Pair finish
resp_pair = os.system('pyvizio --ip=' + cfg.TV_ip + ' pair')
token = input("What is the Challenge Token displayed above: ")
pin = input("What is the pin displayed on the TV: ")
resp_pin = os.system('pyvizio --ip=' + cfg.TV_ip + ' pair_finish --token=' + str(token) + ' --pin=' + str(pin))
AuthToken = input("What is the authentication token displayed above: ")
# Add code to automatically store the auth token
# Currently user needs to manually modify the config file

