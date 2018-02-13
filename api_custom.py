# Basic Flask server that takes commands (intended to be from IFTTT via Google Assistant)
# to trigger scripts that can help automate my living space.
#
# Uses OpenSSL to use https
# Uses logging for logging
# Uses flask_httpauth for authentication
# 
# Server and Authentication
from flask import Flask
from flask_restful import Resource, Api, abort, reqparse
from flask_httpauth import HTTPBasicAuth # for auth
import hashlib # for hashing passwords

# Logging
import logging
from logging.handlers import RotatingFileHandler

# Other
import sys
import time
import subprocess

# Config File
import flask_config as cfg

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

# Callback for retrieving a user's password from the database
def get_pw(username):
    if username in cfg.flask_users:
        return cfg.flask_users.get(username)
    return None

# Callback for hashing a user's incoming password
def hash_pw(username,password):
    return hashlib.sha512(cfg.hash_salt + password).hexdigest()

@auth.verify_password
def verify_pw(username, password):
    stored_pass = get_pw(username)
    ret = (stored_pass == hash_pw(username,password))
    if ret:
        log_good_login(username)
    else:
        log_failed_login(username)
    return ret

# Logges a valid command and uses a basic line/string structure
def log_valid_cmd(user, cls, Cmd):
    cur_time = time.strftime("%c")
    app.logger.info(cur_time + '    ValidCmd   ' +'<'+ user +'>'+ ' '*(15-len(user)) +'  <'+ cls +'>'+ ' '*(15-len(cls)) +'  <'+ Cmd +'>')

# Logges an unknown or invalid command and uses a basic line/string structure
def log_unknown_cmd(user, cls, Cmd):
    cur_time = time.strftime("%c")
    app.logger.info(cur_time + '    UnknownCmd ' +'<'+ user +'>'+ ' '*(15-len(user)) +'  <'+ cls +'>'+ ' '*(15-len(cls)) +'  <'+ Cmd +'>')

# Logges a valid login attempt
def log_good_login(user):
    cur_time = time.strftime("%c")
    app.logger.info(cur_time + '    ValidLogin ' +'<'+ user +'>')

# Logges an invalid login attempt
def log_failed_login(user):
    cur_time = time.strftime("%c")
    app.logger.info(cur_time + '    InvldLogin ' +'<'+ user +'>')


# Resource for controlling a SmartTV
class TVCommand(Resource):
    @auth.login_required
    def get(self, TVCmd):
        cls = 'TVCommand'
        user = auth.username()
        if (TVCmd == "On") or (TVCmd == 'on'):
            execfile("Scripts/TVON.py")
            log_valid_cmd(user, cls, TVCmd)
            ret = 'TV Turned On'
        elif (TVCmd == "Off") or (TVCmd == "off"):
            execfile("Scripts/TVOFF.py")
            log_valid_cmd(user, cls, TVCmd)
            ret = 'TV Turned Off'
        else:
            log_unknown_cmd(user, cls, TVCmd)
            ret = 'Unrecognized TV Command'
            print ret
        return ret, 200

# Resource for controlling a Nest Thermostat
class Nest(Resource):
    @auth.login_required
    def get(self, NestCmd):
        cls = 'Nest'
        user = auth.username()
        if (NestCmd == "Home") or (NestCmd == "home"):
            execfile("Scripts/NestHome.py")
            log_valid_cmd(user, cls, NestCmd)
            ret = 'Nest Set to Home'
        elif (NestCmd == "Away") or (NestCmd == "away"):
            execfile("Scripts/NestAway.py")
            log_valid_cmd(user, cls, NestCmd)
            ret = 'Nest Set to Away'
        else:
            log_unknown_cmd(user, cls, NestCmd)
            ret = 'Unrecognized Nest Command'
        return ret, 200

# Resource for controlling a computer
class CompCommand(Resource):
    @auth.login_required
    def get(self, CompCmd):
        cls = 'CompCommand'
        user = auth.username()
        if CompCmd == "Off":
            execfile("Scripts/CompOFF.py") # Not implemented yet
            log_valid_cmd(user, cls, CompCmd)
            ret = 'Computer turned off'
        elif CompCmd == "Sleep":
            execfile("Scripts/CompSLEEP.py") # Not implemented yet
            log_valid_cmd(user, cls, CompCmd)
            ret = 'Computer set to sleep'
        elif CompCmd == "On":
            execfile("Scripts/CompWOL.py") # Currently run same script as WOL, may implement full power on later
            log_valid_cmd(user, cls, CompCmd)
            ret = 'Computer woken from lan'
        elif CompCmd == "WOL":
            execfile("Scripts/CompWOL.py")
            log_valid_cmd(user, cls, CompCmd)
            ret = 'Computer woken from lan'
        else:
            log_unknown_cmd(user, cls, CompCmd)
            ret = 'Unrecognized Computer Command'
        return ret, 200

class CustomSequence(Resource):
    @auth.login_required
    def get(self, SeqCmd):
        cls = 'CustomSequence'
        user = auth.username()
        if SeqCmd == "LeaveApartment":
            execfile("Scripts/LightsLivingRoomOn.py") # Turns lights on, then back off to verify it works
            execfile("Scripts/CompSLEEP.py")
            execfile("Scripts/NestAway.py")
            execfile("Scripts/TVOFF.py")
            execfile("Scripts/LightsAllOff.py")
            log_valid_cmd(user, cls, SeqCmd)
            ret = 'Sequence for leaving apartment has run'
        elif SeqCmd == "ArriveApartment":
            execfile("Scripts/CompWOL.py")
            execfile("Scripts/NestHome.py")
            execfile("Scripts/LightsLivingRoomOn.py")
            log_valid_cmd(user, cls, SeqCmd)
            ret = 'Sequence for arriving at apartment has run'
        elif SeqCmd == "GoToSleep":
            execfile("Scripts/CompSLEEP.py")
            execfile("LightsLivingRoomOff.py")
            execfile("LightsBedroomOn.py")
            log_valid_cmd(user, cls, SeqCmd)
            ret = 'Sequence for going to sleep has run'
        else:
            log_unknown_cmd(user, cls, SeqCmd)
            ret = 'Unrecognized Sequence Command'
        return ret, 200

# Setup Api resource routing here
# Add a new resource for each command type
api.add_resource(TVCommand, '/TVCommand/<TVCmd>') # Passes through a command to be used in execution
api.add_resource(Nest, '/Nest/<NestCmd>')
api.add_resource(CompCommand, '/CompCommand/<CompCmd>')
api.add_resource(CustomSequence, '/CustomSeq/<SeqCmd>')

if __name__ == '__main__':
    handler = RotatingFileHandler('logfile.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0',ssl_context=('cert.pem','key.pem'),debug=True)



# Use this command to make a new ssl certificate (valid for 365 days):
# openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
