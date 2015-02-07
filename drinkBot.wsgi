#!/usr/local/bin/python
activate_this = '/home/public/drinkBot/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
print sys.path
sys.path.append("/home/public/drinkBot/drinkBot")
print sys.path

from drinkBot import app
if __name__ == '__main__':
	app.run()