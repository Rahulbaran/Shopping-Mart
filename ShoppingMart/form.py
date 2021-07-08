from flask_wtf import FlaskForm 
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, EqualTo, Length, InputRequired, ValidationError
from flask_login import current_user
from ShoppingMart.models import User


# CLASS TO CREATE REGISTER FORM
class RegisterForm(FlaskForm):
    username = StringField(label = 'Username', validators = [InputRequired(), Length(min = 5,max = 50, 
                                                message='username must be 5 to 50 characters long')])
    email = StringField(label = 'Email Address', validators = [InputRequired(), Length(min = 15, max = 60, 
                                                 message = 'email must have atleast 15 characters'), Email(message = 'email address is not valid')])
    password = PasswordField(label = 'Password', validators = [InputRequired(), Length(min = 8, max = 50, 
                                                  message = 'password must be atleast 8 characters long')])
    reenter_password = PasswordField(label = 'Re-enter Password', validators = [InputRequired(), Length(min = 8, max = 50, 
                                                  message = 'password must be atleast 8 characters long'), 
                                                  EqualTo('password', message = 'must be similar to password')])
    submit = SubmitField(label = 'Register')


    # let's work with the custom validators
    def validate_username(self,username):
        invalidChar = '!@#$%^&*()_-+=|\\}]{[?/:;"\'><.,~`'
        tracker = 0
        user = User.query.filter_by(username = username.data).first()
        for char in username.data:
            if char in invalidChar:
                tracker+=1
        if tracker > 0:
            raise ValidationError('username is invalid')
        if user:
            raise ValidationError('username is already taken')


    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('email is already taken')


    def validate_password(self,password):
        specialChar = '!@#$%^&*()_-+=|\\}]{[?/:;"\'><.,~`'
        tracker = 0
        for char in password.data:
            if char in specialChar:
                tracker+=1
        if tracker == 0:
            raise ValidationError('password must have atleast one special character')




# CLASS TO CREATE LOGIN FORM
class LoginForm(FlaskForm):
    email = StringField(label = 'Email Address', validators = [InputRequired(), Length(min = 15, max = 60, 
                                                 message = 'Email must have atleast 15 characters'), Email(message = 'Email address is not valid')])
    password = PasswordField(label = 'Password', validators = [InputRequired(), Length(min = 8, max = 50, 
                                                  message = 'Password must be atleast 8 characters long')])
    remember = BooleanField(label = "Remember Me")
    submit = SubmitField(label = 'Login')



# CLASS TO CREATE UPDATE FORM
class UpdateForm(FlaskForm):
    username = StringField(label = 'Username', validators = [InputRequired(), Length(min = 5,max = 50, 
                                                message='username must be 5 to 50 characters long')])
    email = StringField(label = 'Email Address', validators = [InputRequired(), Length(min = 15, max = 60, 
                                                 message = 'email must have atleast 15 characters'), Email(message = 'email address is not valid')])
    picture = FileField(label = "Upload your picture", validators = [FileAllowed(['gif','jpeg','jpg','png','svg'],message = 'file in gif, jpeg, jpg, png & svg formats are only allowed.')])
    submit = SubmitField(label = 'Update')


    # let's work with the custom validators
    def validate_username(self,username):
        if current_user.username != username.data:
            invalidChar = '!@#$%^&*()_-+=|\\}]{[?/:;"\'><.,~`'
            tracker = 0
            user = User.query.filter_by(username = username.data).first()
            for char in username.data:
                if char in invalidChar:
                    tracker+=1
            if tracker > 0:
                raise ValidationError('username is invalid')
            if user:
                raise ValidationError('username is already taken')


    def validate_email(self,email):
        if current_user.email != email.data :
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('email is already taken')




# reset password request form
class ResetRequestForm(FlaskForm):
    email = StringField(label = "Email Address",validators = [InputRequired(), Length(min = 15, max = 60, 
                                                 message = 'email must have atleast 15 characters'), Email(message = 'email address is not valid')])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError('There is no user with that email')


# reset password form
class ResetPasswordForm(FlaskForm):
    password = PasswordField(label = 'Password', validators = [InputRequired(), Length(min = 8, max = 50, 
                                                  message = 'password must be atleast 8 characters long')])
    reenter_password = PasswordField(label = 'Re-enter Password', validators = [InputRequired(), Length(min = 8, max = 50, 
                                                  message = 'password must be atleast 8 characters long'), 
                                                  EqualTo('password', message = 'must be similar to password')])
    submit = SubmitField(label = 'Reset Password')

    def validate_password(self,password):
        specialChar = '!@#$%^&*()_-+=|\\}]{[?/:;"\'><.,~`'
        tracker = 0
        for char in password.data:
            if char in specialChar:
                tracker+=1
        if tracker == 0:
            raise ValidationError('password must have atleast one special character')