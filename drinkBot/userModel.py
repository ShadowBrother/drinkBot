from __init__ import app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
import datetime

db = SQLAlchemy(app)

engine = db.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True, echo=False)
Base = db.make_declarative_base()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(10))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime, default=datetime.datetime.utcnow)
 
    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        #self.registered_on = datetime.utcnow()
        
    def __repr__(self):
        return '<User %r>' % (self.username)