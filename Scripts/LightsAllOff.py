# Using phue api, turn off all lights
# 
# Users phue. Source: https://github.com/studioimaginaire/phue

from phue import Bridge
import flask_config as cfg

b = Bridge(cfg.hue_ip)
#b.connect() #only have to run once. push Hue link button before running
b.get_api()

lights = b.lights
for l in lights:
    l.on = False

for l in lights:
    print(l.name + '.......' + str(l.on))
