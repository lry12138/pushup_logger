from flask import Blueprint, render_template,url_for,request,redirect
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required
from .models import User
from . import db

auth = Blueprint('auth',__name__)

@auth.route('/register')
def register():
    return render_template('register.html')

@auth.route('/register',methods = ['POST'])
def register_post():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email = email).first()
    if user:
        return redirect(url_for('auth.login'))
    
    else:
        new_user = User(name = name,email = email,password = generate_password_hash(password,method='pbkdf2'))
        db.session.add(new_user)
        db.session.commit()
    
    return redirect(url_for('auth.login'))

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login',methods = ['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email = email).first()
    if not user or not check_password_hash(user.password,password):
        return redirect(url_for('auth.login'))
    
    login_user(user,remember = remember)

    return redirect(url_for('main.profile'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
