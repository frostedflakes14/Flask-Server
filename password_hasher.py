# Must manually create users and store passwords.  This script is used to create the password hash
# that is stored in the config file.

import hashlib

salt = 'Random Stuff' # Random Generated and Stored in Config
code = 'Code to Hash'
hashed = hashlib.sha512(salt + code).hexdigest()
print('Hashed Code: '+ hashed)