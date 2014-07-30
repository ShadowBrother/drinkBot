
from flask import Flask
from flask.ext.login import LoginManager
import logging, sys
logging.basicConfig(stream=sys.stderr)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/drinkBot/drinkBot/cocktails.db'
app.secret_key = 'Tit5M4g33'

#setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
#login_manager.login_view = 'login'

import views
