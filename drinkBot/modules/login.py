from flask import Blueprint, render_template, request, flash, session, redirect, g, jsonify, url_for
from flask.ext.login import login_required, login_user, logout_user, current_user
from drinkBot import login_manager
from drinkBot.userModel import User

loginbp = Blueprint('login', __name__)


login_manager.login_view = 'login'

@loginbp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    #return str(username) + "\n" + str(password)
    if password == "" or username == "":
        flash("Enter username and password", "error")
        return redirect(url_for('login.login'))
    registered_user = User.query.filter_by(username=username,password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('login.login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('drinkBot'))

@loginbp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('drinkBot'))
    
@loginbp.route('/_isLoggedIn')
def isLoggedIn():
    
    return jsonify(loggedIn=g.user.is_authenticated())
	
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))	