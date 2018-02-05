from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
from flask_restful import Resource, Api, abort, reqparse
#from flaskext.auth import Auth

# To launch a .py script in a new terminal window
import sys
import time
import subprocess

app = Flask(__name__)
api = Api(app)
#auth = Auth(app)

parser = reqparse.RequestParser()
#parser.add_argument('task')

# Setup Logging - not implemented completely
"""def setup_logging(app):
  #log_file = app.config.get('LOG_FILE', 'bind9-wapi.log')
  #log_level = app.config.get('LOG_LEVEL', 'INFO')
  handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=1)
  handler.setLevel(log_level)
  app.logger.setLevel(log_level)
  app.logger.addHandler(handler)"""

class TVCommand(Resource):
    def get(self, TVCmd):
        if TVCmd == "On":
            execfile("Scripts/TVON.py")
            ret = 'TV Turned On'
        elif TVCmd == "Off":
            execfile("Scripts/TVOFF.py")
            ret = 'TV Turned Off'
        else:
            ret = 'Unrecognized TV Command'
        return ret, 200

class Nest(Resource):
    def get(self, NestCmd):
        if NestCmd == "Home":
            execfile("Scripts/NestHome.py")
            ret = 'Nest Set to Home'
        elif NestCmd == "Away":
            execfile("Scripts/NestAway.py")
            ret = 'Nest Set to Away'
        else:
            ret = 'Unrecognized Nest Command'
        return ret, 200

class CompCommand(Resource):
    def get(self, CompCmd):
        if CompCmd == "Off":
            execfile("Scripts/CompOFF.py") # Not implemented yet
            ret = 'Computer turned off'
        elif CompCmd == "Sleep":
            execfile("Scripts/CompSLEEP.py") # Not implemented yet
            ret = 'Computer set to sleep'
        elif CompCmd == "On":
            execfile("Scripts/CompWOL.py") # Currently run same script as WOL, may implement full power on later
            ret = 'Computer woken from lan'
        elif CompCmd == "WOL":
            execfile("Scripts/CompWOL.py")
            ret = 'Computer woken from lan'
        else:
            ret = 'Unrecognized Computer Command'
        return ret, 200

# Setup Api resource routing here
# Add a new resource for each command type
api.add_resource(TVCommand, '/TVCommand/<TVCmd>') # Passes through a command to be used in execution
api.add_resource(Nest, '/Nest/<NestCmd>')
api.add_resource(CompCommand, '/CompCommand/<CompCmd>')

if __name__ == '__main__':
    app.run(debug=True)
