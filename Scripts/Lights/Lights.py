# Prototype Script to turn on Light[3]
# 
# Users phue. Source: https://github.com/studioimaginaire/phue
"""
from phue import Bridge
import flask_config as cfg

b = Bridge(cfg.hue_ip)
#b.connect() #only have to run once. push Hue link button before running
b.get_api()

lights = b.lights
for l in lights:
    print(l.name + '.....' + str(l.on))
    
lights[3].on = True
"""

# Using phue api, turn on Living Room
# 
# Users phue. Source: https://github.com/studioimaginaire/phue

from phue import Bridge
from phue import Group
import flask_config as cfg
import time

b = Bridge(cfg.hue_ip)
#b.connect() #only have to run once. push Hue link button before running
b.get_api()

group_living = Group(b, 'Living room')
#group_living.on = True
#group_living.brightness = 254


#print group_living.on
#group_living.brightness = 254
#print group_living.brightness
#print group_living.colormode
ran = [0,5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55000,60000,65535]
print ran

for i in ran:
    group_living.hue = i
    print i
    print group_living.hue
    time.sleep(2)
#group_living.saturation = 254
#print group_living.saturation
#group_living.xy = [[0.5, 0.5]]
#print group_living.xy
#print group_living.colortemp
#print group_living.effect
#print group_living.alert

