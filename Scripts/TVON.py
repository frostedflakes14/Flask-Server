# Uses pyvizio api to send TV On or Off command
# You must first go through a pairing process to get an auth token from the tv
# before you can send commands
#
# API Source Link: https://github.com/vkorn/pyvizio
#
# I spent more time then it was worth trying to create a specific script to run
# the power on/off command. It ended up being easier just to run the command
# using 'os.system'

import os
import flask_config as cfg

# Using pyvizio send this command in terminal:
# sudo pyvizio --ip=<TV IP address> --auth=<your auth token> power on
os.system('sudo pyvizio --ip=' + cfg.TV_ip + ' --auth=' + cfg.auth_token + ' power on')

print("Turned TV On")