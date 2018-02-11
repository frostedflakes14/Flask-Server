# Must manually create users and store passwords.  This script is used to create the password hash
# that is stored in the config file.

from flask_httpauth import HTTPBasicAuth
from hashlib import md5

code = 'password to hash'
hashed = md5(code).hexdigest()
print hashed