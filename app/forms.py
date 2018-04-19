from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, DataRequired


class ProfileForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired()]) 
    lastname = StringField('Last Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Female, Female', 'Male, Male')], validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    photo = FileField('Add Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'Photo Only!'])])
    bio = TextField('Biography', validators=[DataRequired()])
    
# class LoginForm(FlaskForm):
#     username = StringField('Username', validators=[InputRequired()])
#     password = PasswordField('Password', validators=[InputRequired()])
