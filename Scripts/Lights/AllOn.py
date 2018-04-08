# Using phue api, turn on all lights
# 
# Users phue. Source: https://github.com/studioimaginaire/phue

from phue import Bridge
import flask_config as cfg

b = Bridge(cfg.hue_ip)
#b.connect() #only have to run once. push Hue link button before running
b.get_api()

lights = range(1,101,1) # Creates array of 1-100 (hue bulbs start at 1)
b.set_light(lights, {'on':True, 'bri':254, 'sat':0})

print "Turned all lights on"

