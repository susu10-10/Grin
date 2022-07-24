from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, EqualTo
from grin.models import User


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log in')



class RegisterForm(FlaskForm):
    fullname = StringField('Full name:',
                            validators=[DataRequired()])
    email = StringField('Email:', 
                        validators=[Email(), DataRequired()])
    password = PasswordField('Password:',
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password:', 
                                validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


    def validate_email(self, email):
        #check if user submitted is already in our database
        user = User.query.filter_by(email=email.data).first()
        if user: #if user is none then no error but if there is already a user with that name then throw an error
            raise ValidationError('That Email is taken. Please choose another one.')
