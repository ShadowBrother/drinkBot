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
        
        if (request.form.get("availableOnly")):#availableOnly checkbox is checked
            availableOnly = True
        else:
            availableOnly = False
        return render_template("drinkBot.html", drinks = Drink.query.filter(Drink.name.like('%' + request.form["search"] + '%')).all(), availableOnly = availableOnly)
    else:#serve up normal page that lists all available drinks
        availableOnly = request.args.get("availableOnly")#check if URL has availableOnly set
        if availableOnly is None or availableOnly != "False":
            availableOnly = True# show available only by default
        else:
            availableOnly = False
        
        return render_template("drinkBot.html", drinks = Drink.query.all(), availableOnly = availableOnly )

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
            #flash(amount + "  " + name)
            order.append(amount + "  " + name + "\n")
        return "Order: " + "".join(order)
            
    else:
        flash("No amount specified.")
    return redirect(url_for('drinkBot'))
    #return render_template('order.html', order=orderObj)

@app.route('/db/_confirmRecipe', methods=['POST'])
@login_required
def confirm_recipe():
    if(request.form.get("amount") and request.form.get("name")):
        order=[]
        #TODO:
            
            #ability to add glass size?
        
        #for each tuple, check if liquid_name exists in liquids db and get liquid_id if it does, else ask if should enter or abort
        #check if row exists in Mix with drink_id and liquid_id
        #    if yes, update row, else insert
        #check if any liquids in Mix for drink are missing in new recipe, need to delete those from Mix
        
        recipe = zip(request.form.getlist("amount"), request.form.getlist("name")) ;
        if(recipe):
            
            drinkName = request.form.get("drinkName").strip()
            drink = Drink.query.filter_by(name=drinkName).first()
            if(not drink):
                    
                    flash(drinkName + " is not in Drinks table. If you do not want to add " + drinkName + " to database hit Cancel.")
                    #return name + " not found."
                
            for amount, name in recipe:
                #flash(amount + "  " + name)
                #order.append(amount + "  " + name + "\n")
                liquid = Liquid.query.filter_by(name=name.strip()).all()
                
                
                if(not liquid):
                    
                    flash(name + " is not in Liquids table. If you do not want to add " + name + " to database hit Cancel.")
                    #return name + " not found."
                
            return render_template('confirmRecipe.html', drinkName=drinkName, recipe=recipe)
            
            
    flash("Please fill in all fields.")
    return redirect(url_for('drinkBot'))
    
@app.route('/db/_saveRecipe', methods=['POST'])
@login_required
def save_recipe():
    #TODO:
        #remove rows from mix of ingredients that have been removed from recipe
        #create template page or have it redirect to drinkBot with search set to just added drink
        #test code


    #for each tuple, check if liquid_name exists in liquids table and get liquid_id if it does, else add to liquids table
        #check if row exists in Mix with drink_id and liquid_id
        #    if yes, update row, else insert
        #check if any liquids in Mix for drink are missing in new recipe, need to delete those from Mix
    if(request.form.get("amount") and request.form.get("name")):
        
        
        amountList = request.form.getlist("amount")
        nameList = request.form.getlist("name")
        recipe = zip(amountList, nameList ) ;
        if(recipe):
            
            drinkName = request.form.get("drinkName").strip()
            drink = Drink.query.filter_by(name=drinkName).first()#check if drink is in Drink table
            
            if(not drink):#add drink to Drink table
                try:
                    db.session.add(Drink(drinkName))
                    db.session.commit()
                    drink = Drink.query.filter_by(name=drinkName).first()
                    flash(drink.name + " added to Drinks table.")
                    
                except:
                    db.session.rollback()
                    raise
            

            #iterate through mix rows for drinkName and remove rows for ingredients no longer in recipe
            mixes = drink.mixes
            for mix in mixes:
                if mix.liquid.name not in nameList:
                    try:
                        db.session.delete(mix)
                        db.session.commit()
                    except:
                        db.session.rollback()
                        raise
                        
            #iterate through recipe, adding liquids to liquid table as needed, adding/updating mix table as needed
            for amount, name in recipe:
                
                
                
                liquid = Liquid.query.filter_by(name=name.strip()).first()#try and find liquid in Liquid table
                
                
                if(not liquid):#liquid is not in table, add it to table
                    
                    liquid = Liquid(name.strip())
                    try:
                        db.session.add(liquid)
                        db.session.commit()
                        liquid = Liquid.query.filter_by(name=liquid.name).first()
                        flash(liquid.name + " added to liquid table")
                    except:
                        db.session.rollback()
                        raise
                    
                mix = Mix.query.filter_by(drink_id=drink.id).filter_by(liquid_id=liquid.id).first()#try to find matching mix row
                
                if(not mix):#ingredient was not originally in mix, add it
                    try:
                        db.session.add(Mix(drink, liquid, amount))
                        db.session.commit()
                        flash(liquid.name + " added to mix with amount " + amount)
                    except:
                        db.session.rollback()
                        raise
                        
                else:#ingredient was in mix, need to update amount
                    try:
                        #Mix.update().values(amount=amount).where(and(Mix.c.drink_id=drink.id, Mix.c.liquid_id=liquid.id))
                        mix.amount = amount
                        db.session.commit()
                        flash(liquid.name + " updated with new amount " + amount)
                    except:
                        db.session.rollback()
                        raise
            return redirect(url_for("drinkBot"))
            
            
    flash("Error: No recipe.")
    return redirect(url_for('drinkBot'))

@app.route('/db/_deleteRecipe', methods=['POST'])
@login_required
def delete_recipe():
    drinkName = request.form.get("drinkName").strip()
    if(drinkName):
        drink = Drink.query.filter_by(name=drinkName).first()
        if(drink):
            try:
                db.session.delete(drink)
                db.session.commit()
                flash(drinkName + " deleted.") 
            except:
                db.session.rollback()
                raise
        else:
            flash("No drink " + drinkName + " found.")
    else:
        flash("No drink name entered.", "error")
    return redirect(url_for('drinkBot'))
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