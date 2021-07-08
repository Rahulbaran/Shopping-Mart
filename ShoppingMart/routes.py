import secrets
import os
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from ShoppingMart import app, db, bcrypt, mail
from ShoppingMart.form import RegisterForm, LoginForm, UpdateForm, ResetRequestForm, ResetPasswordForm
from ShoppingMart.models import User, Items, UserItems
from flask_mail import Message



# creating routes
@app.route('/')
def home():
    return render_template('home.html', title="Shopping Mart || One Place for all products")
app.add_url_rule('/home','home',home)


@app.route('/market')
def market():
    allItems = Items.query.all()
    return render_template('market.html', title = "Market",items = allItems)


@app.route('/market/purchase/<int:product_id>',methods=['GET','POST'])
def purchase_product(product_id):
    if current_user.is_authenticated == False:
        flash('Please login to purchase any product','info')
        return redirect(url_for('login'))
    item = Items.query.filter_by(barCode=product_id).first()
    userItem = UserItems(itemname=item.item, amount=item.amount, 
                        barCode=item.barCode, customer=current_user)
    if item:
        db.session.delete(item)
        db.session.add(userItem)
        current_user.totalBudget -= int(item.amount)
        if current_user.totalBudget < 0:
            current_user.totalBudget = 15000
        db.session.commit()
        flash(f'you have purchased a product:- {item.info}','info')
        return redirect(url_for('market'))
    else:
        flash('Sorry product is not available','info')
        return redirect(url_for('market'))




@app.route('/register', methods=['GET','POST'])
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



# function to save picture in the memory
def save_pic(pic):
    random_hex = secrets.token_hex(8)
    _, pic_ext = os.path.splitext(pic.filename)
    newPic = random_hex + pic_ext
    path = os.path.join(app.root_path,'static','Images',newPic)
    pic.save(path)
    return newPic


@app.route('/account',methods = ['POST','GET'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_pic(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('You have updated your account','info')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    picture = url_for('static',filename=f'Images/{current_user.image_file}')
    userItems = UserItems.query.all()
    return render_template('account.html',title='Account',form = form,
                                         picture = picture, allItems = userItems)



# route to sell item
@app.route('/account/product/<int:product_id>', methods=['POST','GET'])
@login_required
def sell_product(product_id):
    userItem = UserItems.query.filter_by(barCode=product_id).first()
    item = Items(item=userItem.itemname,barCode=userItem.barCode,amount=userItem.amount,info='Hello World')
    if item:
        db.session.delete(userItem)
        db.session.add(item)
        current_user.totalBudget += int(item.amount)
        if current_user.totalBudget > 15000:
            current_user.totalBudget = 15000
        db.session.commit()
        flash(f'you have sold a product:- {item.info}','info')
        return redirect(url_for('market'))



# function to send token
def send_token(user):
    token = user.get_reset_token()
    msg = Message('Reset Password',recipients = [user.email])
    msg.body = f'''To reset password , visit the following link:
{url_for('reset_token',token = token, _external = True)}

If you did not make this request then simply ignore this email and no change will be made'''
    mail.send(msg)

# routes for resetting password
@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_token(user)
        flash('An email has been delivered in email address to reset password','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form = form, title='Request Password Reset')


@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token','info')
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_pw
        db.session.commit()
        flash('Your password has been updated, now you are able to login','info')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form = form)
