# Uses the Nest-thermostat api to set your Nest to Home
# 
# source: https://github.com/FiloSottile/nest_thermostat/

import sys
from optparse import OptionParser
from nest_thermostat import Nest
import requests
import flask_config as cfg

# Get Nest Data
# Creates Parser
parser = OptionParser(usage="nest [options] command [command_options] [command_args]",
                      description="Commands: fan temp", version="unknown")
parser.add_option("-u", "--user", dest="user",
                  help="username for nest.com", metavar="USER", default=None)
parser.add_option("-p", "--password", dest="password",
                  help="password for nest.com", metavar="PASSWORD", default=None)
parser.add_option("-c", "--celsius", dest="celsius", action="store_true", default=False,
                  help="use celsius instead of farenheit")
parser.add_option("-s", "--serial", dest="serial", default=None,
                  help="optional, specify serial number of nest thermostat to talk to")
parser.add_option("-i", "--index", dest="index", default=0, type="int",
                  help="optional, specify index number of nest to talk to")

(opts, args) = parser.parse_args() #must keep this unless you want to specify all options from the parser (celsius, serial etc
opts.user = cfg.nest_user #nest email
opts.password = cfg.nest_pass #nest password
opts.serial = None
opts.index = 0
args = []
units = "F"
n = Nest(opts.user, opts.password, opts.serial, opts.index, units=units)
n.login()
n.get_status()

response = requests.post(n.transport_url + "/v2/put/structure." + n.structure_id,
                         data = '{"away":%s}' % ('false'),
                         headers = {"user-agent":"Nest/1.1.0.10 CFNetwork/548.0.4",
                                    "Authorization":"Basic " + n.access_token,
                                    "X-nl-protocol-version": "1"})
response.raise_for_status()

print("Nest set to Home")
