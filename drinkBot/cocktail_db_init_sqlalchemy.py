from __init__ import app
from flask.ext.sqlalchemy import SQLAlchemy
from dbModels import Drink, Liquid, Mix, Inventory, db, engine

db.drop_all()
db.create_all() 
    
#Gin and Tonic
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

db.session.add(Inventory(gin,1))
db.session.add(Inventory(tonic,2))
#Rum and Coke
rum = Liquid('Rum')
coke = Liquid('Coke')
rumandcoke = Drink('Rum and Coke', 3.50)
db.session.add(Mix(rumandcoke, rum, 33.33))
db.session.add(Mix(rumandcoke, coke, 33.33))
db.session.add(Inventory(coke,3))

#Jack and Coke
jack = Liquid('Jack Daniels')
jackandcoke = Drink('Jack and Coke', 4.00)
db.session.add(Mix(jackandcoke, jack, 25.0))
db.session.add(Mix(jackandcoke, coke, 75.00))
db.session.add(Inventory(jack))

#Vodka Martini
vodka = Liquid('Vodka')
vermouth = Liquid('Vermouth')
vodkamartini = Drink('Vodka Martini')
db.session.add(Mix(vodkamartini, vodka, 33.33))
db.session.add(Mix(vodkamartini, vermouth, 66.66))
db.session.add(Inventory(vermouth))
db.session.add(Inventory(vodka, 4))


db.session.commit()