import os
from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from form import RegisterForm, LoginForm

# initiating the application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# database tables using sqlalchemy
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(60), unique = True, nullable = False)
    totalBudget = db.Column(db.Integer, default = 15000)
    password = db.Column(db.Integer, nullable = False)
    image_file = db.Column(db.String, nullable = False, default = 'default.png')
    items = db.relationship('UserItems', backref = 'customer', lazy = True)


class UserItems(db.Model):
    __tablename__ = 'userItems'
    id = db.Column(db.Integer, primary_key = True)
    itemname = db.Column(db.String, nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    date_bought = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)


class Items(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key = True)
    item = db.Column(db.String, nullable = False)
    amount = db.Column(db.Integer, nullable = False)
    info = db.Column(db.String, nullable = False)




# creating routes
@app.route('/')
def home():
    return render_template('home.html', title="Shopping Mart || One Place for all products")
app.add_url_rule('/home','home',home)


@app.route('/market')
def market():
    return render_template('market.html', title="Market")


@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash('Congratulations, You are now a member of our family','info')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form = form)


@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title="Login", form = form)



