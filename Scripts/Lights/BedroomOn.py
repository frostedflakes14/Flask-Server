# Using phue api, turn on bedroom lights
# 
# Users phue. Source: https://github.com/studioimaginaire/phue

from phue import Bridge
import flask_config as cfg

b = Bridge(cfg.hue_ip)
#b.connect() #only have to run once. push Hue link button before running
b.get_api()

b.set_group('Bedroom', {'on':True, 'bri':254})

print "Turned on bedroom lights"


