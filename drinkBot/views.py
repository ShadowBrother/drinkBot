from __init__ import app, login_manager
from flask import render_template, request, flash, session, redirect, url_for, g, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import login_required, login_user, logout_user, current_user
from dbModels import Drink, Liquid, Mix, Inventory, db, engine
from userModel import User

#login_manager.init_app(app)
login_manager.login_view = 'login'

@app.route('/')
def hello_world():
    return 'You cannot get ye Flask!'

@app.route('/num/<int:n>')
def print_n(n):
    return str(n)

@app.route('/db', methods=['GET', 'POST'])
def drinkBot():
    
    #db.create_all()
    
    if (request.method == 'POST'):#post method means user used searchbar
        flash(request.form.get("amount"))
        if (request.form.get("availableOnly")):#availableOnly checkbox is checked
            availableOnly = True
        else:
            availableOnly = False
        return render_template("drinkBot.html", drinks = Drink.query.filter(Drink.name.like('%' + request.form["search"] + '%')).all(), availableOnly = availableOnly)
    else:#serve up normal page that lists all available drinks
        return render_template("drinkBot.html", drinks = Drink.query.all(), availableOnly = True)

@app.route('/db/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    if(request.method == 'POST'):
        if(request.form.get('removeBtn')):
            #deleted = []
            for liquid in request.form.getlist("checkbox"):
                liqStr = str(liquid)[:-1]#take substring to cut off trailing "\" that get's added for some reason
                #deleted.append(Inventory.query.filter(Inventory.id==liqStr).one().liquid.name + " ")
                flash(Inventory.query.filter(Inventory.id==liqStr).one().liquid.name + " deleted")
                Inventory.query.filter(Inventory.id==liqStr).delete()#delete from inventory
                
            #flash("".join(deleted) + " deleted")
            db.session.commit()
            return render_template("inventory.html", inventory = Inventory.query.all())
        elif(request.form.get('addBtn')):
            newInvStr = request.form.get('add')
            liq = Liquid.query.filter(Liquid.name==newInvStr).first()
            if(liq == None):
                guess = Liquid.query.filter(Liquid.name.like('%' + newInvStr + '%')).first()
                flash( "No drink with that name.")
                if (guess is not None):
                    flash("Did you mean: " + guess.name)
                return redirect(url_for('inventory'))
            else:
                newInv = Inventory(liq)
                
                if(newInv == None):
                    flash( "ERROR creating Inventory object")
                    return redirect(url_for('inventory'))
                else:
                    #return str(Inventory.query.filter(Inventory.liquid_id == newInv.liquid.id).first())
                    if(Inventory.query.filter(Inventory.liquid_id == newInv.liquid.id).first() is not None):
                        flash("Already in Inventory")
                        return redirect(url_for('inventory'))
                        
                    db.session.add(newInv)
                    db.session.commit()
                    
    return render_template("inventory.html", inventory = Inventory.query.all())

@app.route('/db/_order', methods=['POST'])
def order():
    if(request.form.get("amount")):
        order=[]
                
        for amount, name in zip(request.form.getlist("amount"), request.form.getlist("name")):
            flash(amount + "  " + name)
            order.append(amount + "  " + name + "\n")
        return "".join(order)
            
    else:
        flash("No amount specified.")
    return redirect(url_for('drinkBot'))
    #return render_template('order.html', order=orderObj)
    
#login routes
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

    
@app.route('/db/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    #return str(username) + "\n" + str(password)
    if password == "" or username == "":
        flash("Enter username and password", "error")
        return redirect(url_for('login'))
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('drinkBot'))

@app.route('/db/logout')
def logout():
    logout_user()
    return redirect(url_for('drinkBot'))
    
@app.route('/db/_isLoggedIn')
def isLoggedIn():
    
    return jsonify(loggedIn=g.user.is_authenticated())