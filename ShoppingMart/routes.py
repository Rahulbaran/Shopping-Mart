from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from ShoppingMart import app, db, bcrypt, login_manager
from ShoppingMart.form import RegisterForm, LoginForm, UpdateForm
from ShoppingMart.models import User, Items, UserItems



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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, You are now a member','info')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form = form)



@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember = form.remember.data)
            next = request.args.get('next')
            flash('You have logged in','info')
            return redirect(next) if next else redirect(url_for('home'))
        else:
            flash('Either email address or password is wrong','warning')
    return render_template('login.html', title="Login", form = form)



@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out','info')
    return redirect(url_for('home'))



@app.route('/account',methods = ['POST','GET'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You have updated your account','info')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html',title='Account',form = form)


