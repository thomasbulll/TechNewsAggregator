from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from database.user.get_user import check_email_exists, check_username_exists


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_repeat = PasswordField('Password (Repeated)', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username: StringField):
        if check_username_exists(username.data) is not None:
            raise ValidationError('Username already exists')

    def validate_email(self, email: StringField):
        if check_email_exists(email.data) is not None:
            raise ValidationError('Email already exists')

class EmailNotificationForm(FlaskForm):
    key_word = StringField('Key word to filter', validators=[DataRequired()])
    submit = SubmitField('Create Email Filter')
