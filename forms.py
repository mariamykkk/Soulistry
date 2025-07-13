from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BioForm(FlaskForm):
    blood_type = StringField('Blood Type', validators=[DataRequired()])
    eye_color = StringField('Eye Color', validators=[DataRequired()])
    origin = StringField('Origin', validators=[DataRequired()])
    mood = StringField('Current Mood', validators=[DataRequired()])
    submit = SubmitField('Generate Melody')
