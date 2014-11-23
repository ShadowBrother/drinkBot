from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////var/www/drinkBot/cocktails.db'
db = SQLAlchemy(app)

engine = db.create_engine('sqlite:////var/www/drinkBot/cocktails.db', convert_unicode=True, echo=False)
Base = db.make_declarative_base()
Base.metadata.reflect(engine)


#db models - to be moved to models.py?
class Liquid(db.Model):
   # __table__ = Base.metadata.tables['Liquids']
    __tablename__ = 'Liquids'
    __table_args__ = {'autoload': True, 'autoload_with': engine}
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(80))
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Liquid %r>' % self.name


class Drink(db.Model):
    #__table__ = Base.metadata.tables['Drinks']
    
    __tablename__ = 'Drinks'
    __table_args__ = {'autoload': True, 'autoload_with': engine}
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(80))
    # price = db.Column(db.Float)

    def __init__(self, name, price):

        self.name = name
        self.price = price

    def __repr__(self):
        return '<Drink %r>' % self.name

class Mix(db.Model):
    __tablename__ = 'Mix'
    __table_args_ = {'autoload': True, 'autoload_with': engine}
    #__table__ = Base.metadata.tables['Mix']
    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column('drink_id', db.Integer, db.ForeignKey('Drinks.id'))
    drink = db.relationship('Drink', backref=db.backref('Drinks', lazy='dynamic'), primaryjoin = (Drink.id == drink_id))
    liquid_id = db.Column(db.Integer, db.ForeignKey('Liquids.id'))
    liquid = db.relationship('Liquid', backref=db.backref('liquids', lazy='dynamic'), primaryjoin = (Liquid.id == liquid_id))
   # amount = db.Column(db.Integer)

    def __init__(self, drink, liquid, amount):
        self.drink = drink
        self.liquid = liquid
        self.amount = amount

    def __repr__(self):
        return '<Mix %r, %r>' % (self.drink.name, self.liquid.name)

class Inventory(db.Model):
    __table__ = Base.metadata.tables['Inventory']
    #id = db.Column(db.Integer, primary_key=True)
    #liquid_id = db.Column(db.Integer, db.ForeignKey('liquid.id'))
    #liquid = db.relationship('Liquid')


    def __init__(self, liquid):
        self.liquid = liquid

    def __repr__(self):
        return '<Inventory %r>' % self.liquid.name

#routes
@app.route('/')
def hello_world():
    return 'You cannot get ye Flask!'

@app.route('/num/<int:n>')
def print_n(n):
    return str(n)

@app.route('/db/')
def drinkBot():
    


    db.create_all()
    
    # gin = Liquid('Gin')
    # tonic = Liquid('Tonic')
    # ginAndTonic = Drink('Gin and Tonic', 3.00)
    # db.session.add(gin)
    # db.session.add(tonic)
    # db.session.add(ginAndTonic)
    # ginAndTonicMix1 = Mix(ginAndTonic, gin, 1)
    # ginAndTonicMix2 = Mix(ginAndTonic, tonic, 1)
    # db.session.add(ginAndTonicMix1)
    # db.session.add(ginAndTonicMix2)
    
    # db.session.commit()
    

    output = []
    # output.append(repr(gin))
    # output.append("\n")
    # output.append(str(ginAndTonic))
    # output.append("\n")
    # output.append(str(ginAndTonicMix1))
    # output.append("\n")
    # output.append(str(ginAndTonic.drinks.all()))
    # output.append("\n")
    # output.append(str(gin.liquids.all()))
    # output.append("\n")
    # output.append(str(Mix.query.all()))
    # mixes = Mix.query.all()
    # for mix in mixes:
    #     output.append(str(mix.liquid))
    #     output.append("\n")
    #return ''.join(output)

    db_session = db.scoped_session(db.sessionmaker(bind=engine))
    for item in db_session.query(Mix).all():
        output.append(str(item) + "\n")

    # for item in db.session.query(Mix).all():
    #     output.append(str(item))

    # output.append("\n")
    # for item in Mix.query.all():
    #     output.append(str(item))
    # return ''.join(output)
    output.append("\n" + str(Drink.query.first()))
    output.append("\n" + str(Liquid.query.first()))
    output.append("\n" + str(Mix.query.filter_by(drink_id = 3).first()))
    output.append("\n" + str(Mix.query.filter_by(drink_id = 3).first().drink.name))
    
    return '<pre>' + ''.join(output).replace('<', '&lt;').replace('>', '&gt;') + '</pre>' 
    #return "drink: " + str(Drink.query.first())

if __name__ == '__main__':
    app.run(host='0.0.0.0')
