from __init__ import app
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

engine = db.create_engine('sqlite:////var/www/drinkBot/drinkBot/cocktails.db', convert_unicode=True, echo=False)
Base = db.make_declarative_base()
#Base.metadata.reflect(engine)




#db models

class Inventory(db.Model):
    __tablename__ = 'Inventory' #Base.metadata.tables['Inventory']
    #__table_args__ = {'autoload': True, 'autoload_with': engine}
    id = db.Column(db.Integer, primary_key=True)
    liquid_id = db.Column(db.Integer, db.ForeignKey('Liquids.id'), unique=True)
    slot = db.Column(db.Integer, unique=True)#slot in robot drink is in (one slot for each solenoid)


    def __init__(self, liquid, slot=None):
        self.liquid = liquid
        self.slot = slot 
    def __repr__(self):
        return '<Inventory %r>' % self.liquid.name


class Liquid(db.Model):
   # __table__ = Base.metadata.tables['Liquids']
    __tablename__ = 'Liquids'
    #__table_args__ = {'autoload': True, 'autoload_with': engine}
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(80), unique=True)
    inventory = db.relationship('Inventory', backref="liquid", primaryjoin = (Inventory.liquid_id == id))
    
    def available(self):#True if Liquid is in Inventory, else False
        if(self.inventory):
            return True
        else:
            return False
            
    def in_bot(self):#True if Liquid is in Inventory and assigned a slot in robot
        
        if( self.available() and self.inventory[0].slot is not None):
            return True
        else:
            return False

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Liquid %r>' % self.name


class Drink(db.Model):
    #__table__ = Base.metadata.tables['Drinks']
    
    __tablename__ = 'Drinks'
    #__table_args__ = {'autoload': True, 'autoload_with': engine}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    price = db.Column(db.Float)
    

    def available(self):#returns True if all ingredients required are in Inventory
        for ing in self.mixes:
            if (not ing.liquid.available()):
                return False
        return True
    
    def all_in_bot(self):#returns True if all ingredients required are in robot
        for ing in self.mixes:
            if(not ing.liquid.in_bot()):
                return False
        return True

    def __init__(self, name, price= 0.0):

        self.name = name
        self.price = price

    def __repr__(self):
        return '<Drink %r>' % self.name

class Mix(db.Model):
    __tablename__ = 'Mix'
    #__table_args__ = {'autoload': True, 'autoload_with': engine}
    #__table__ = Base.metadata.tables['Mix']
    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column('drink_id', db.Integer, db.ForeignKey('Drinks.id'))
    drink = db.relationship('Drink', backref=db.backref('mixes', lazy='dynamic', cascade='all, delete'), primaryjoin = (Drink.id == drink_id))
    liquid_id = db.Column(db.Integer, db.ForeignKey('Liquids.id'))
    liquid = db.relationship('Liquid', backref=db.backref('mixes', lazy='dynamic'), primaryjoin = (Liquid.id == liquid_id))
    amount = db.Column(db.Float)#percentage


    def __init__(self, drink, liquid, amount):
        self.drink = drink
        self.liquid = liquid
        self.amount = amount

    def __repr__(self):
        return '<Mix %r, %r>' % (self.drink.name, self.liquid.name)

