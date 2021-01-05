from app.models import User
from flask_wtf import FlaskForm
from wtforms.widgets import TextArea 
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo

class EditBioForm(FlaskForm):
    bio = TextAreaField('Bio', widget=TextArea())
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')

class CreatePostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text')
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit')
