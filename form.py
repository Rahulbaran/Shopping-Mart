from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, EqualTo, Length, InputRequired



# CLASS TO CREATE REGISTER FORM
class RegisterForm(FlaskForm):
    username = StringField(label = 'Username', validators = [InputRequired(), Length(min = 5,max = 50, 
                                                message='Username must be 5 to 50 characters long')])
    email = StringField(label = 'Email Address', validators = [InputRequired(), Length(min = 15, max = 60, 
                                                 message = 'Email must have atleast 15 characters'), Email(message = 'Email address is not valid')])
    password = PasswordField(label = 'Password', validators = [InputRequired(), Length(min = 8, max = 50, 
                                                  message = 'Password must be atleast 8 characters long')])
    reenter_password = PasswordField(label = 'Re-enter Password', validators = [InputRequired(), Length(min = 8, max = 50, 
                                                  message = 'Password must be atleast 8 characters long'), 
                                                  EqualTo('password', message = 'Reenter-password must be similar to password')])
    submit = SubmitField(label = 'Register')



# CLASS TO CREATE LOGIN FORM
class LoginForm(FlaskForm):
    email = StringField(label = 'Email Address', validators = [InputRequired(), Length(min = 15, max = 60, 
                                                 message = 'Email must have atleast 15 characters'), Email(message = 'Email address is not valid')])
    password = PasswordField(label = 'Password', validators = [InputRequired(), Length(min = 8, max = 50, 
                                                  message = 'Password must be atleast 8 characters long')])
    submit = SubmitField(label = 'Login')