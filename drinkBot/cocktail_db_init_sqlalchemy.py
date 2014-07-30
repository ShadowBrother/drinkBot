from __init__ import app
from flask.ext.sqlalchemy import SQLAlchemy
from dbModels import Drink, Liquid, Mix, Inventory, db, engine

db.drop_all()
db.create_all()
    
gin = Liquid('Gin')
tonic = Liquid('Tonic')
ginAndTonic = Drink('Gin and Tonic', 3.00)
db.session.add(gin)
db.session.add(tonic)
db.session.add(ginAndTonic)
ginAndTonicMix1 = Mix(ginAndTonic, gin, 50)
ginAndTonicMix2 = Mix(ginAndTonic, tonic, 50)
db.session.add(ginAndTonicMix1)
db.session.add(ginAndTonicMix2)

db.session.add(Inventory(gin))
db.session.add(Inventory(tonic))

rum = Liquid('Rum')
coke = Liquid('Coke')
rumandcoke = Drink('Rum and Coke', 3.50)
db.session.add(Mix(rumandcoke, rum, 33.33))
db.session.add(Mix(rumandcoke, coke, 33.33))
db.session.add(Inventory(coke))

db.session.commit()