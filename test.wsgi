activate_this = '/var/www/drinkBot/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


from hello import app as application