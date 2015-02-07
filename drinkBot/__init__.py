
from flask import Flask
from flask.ext.login import LoginManager
import logging, sys
#from reverseProxied import ReverseProxied
from url_forFix import routeFix
from jinja2 import Environment, PackageLoader



logging.basicConfig(stream=sys.stderr)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/public/drinkBot/drinkBot/db/cocktails.db'
app.config['APPLICATION_ROOT'] = '/flask/'
app.secret_key = 'Tit5M4g33'
#app.wsgi_app = ReverseProxied(app.wsgi_app)

#from drinkBot.bp import bp
#app.register_blueprint(bp)

#setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'


app.jinja_env.filters['routeFix'] = routeFix

import drinkBot.views

#if __name__ == '__main__':
#	app.run()