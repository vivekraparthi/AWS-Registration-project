from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db


auth = Blueprint('auth', __name__) 

@auth.route('/login', methods=['GET', 'POST']) 
def login(): 
    if request.method=='GET': 
        return render_template('login.html')
    else: 
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup(): 
    if request.method=='GET':
        return render_template('signup.html')
    else:
        email = request.form.get('email')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('password')

        file = request.files['file']
        file1 = request.files['file']
        words = file1.read()
        wc = len(words.split())

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        new_user = User(email=email, firstname=firstname,lastname=lastname, password=generate_password_hash(password, method='sha256'),filename = file.filename,data=file.read(),wc=wc) 
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))

@auth.route('/logout') 
@login_required
def logout(): 
    logout_user()
    return redirect(url_for('main.index'))