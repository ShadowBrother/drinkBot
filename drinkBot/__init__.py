
from flask import Flask, Blueprint
from flask.ext.login import LoginManager
from flask.ext.rq import RQ, get_worker
import logging, sys
#from reverseProxied import ReverseProxied
from url_forFix import routeFix
from jinja2 import Environment, PackageLoader



logging.basicConfig(stream=sys.stderr)
app = Flask(__name__)

app.config.from_object('config')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/drinkBot/drinkBot/db/cocktails.db'
#app.config['APPLICATION_ROOT'] = '/flask/'
#app.config['MAX_SLOTS'] = 4

app.secret_key = 'Tit5M4g33'
#app.wsgi_app = ReverseProxied(app.wsgi_app)

#create redis queue instance
RQ(app)



#setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'


app.jinja_env.filters['routeFix'] = routeFix

#views

from modules.login import loginbp

app.register_blueprint(loginbp, url_prefix='/db')


import drinkBot.views

#if __name__ == '__main__':
#	app.run()