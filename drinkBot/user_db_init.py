from __init__ import app
from flask.ext.sqlalchemy import SQLAlchemy
from userModel import User, db

db.drop_all()
db.create_all()

db.session.add(User('admin', 'admin', 'jesselhoyt@gmail.com'))
db.session.add(User('guest', 'guest',""))

db.session.commit()