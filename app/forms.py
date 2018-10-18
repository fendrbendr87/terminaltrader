from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, RadioField, Form, SelectField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import accounts

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
            'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    balance = IntegerField('Balance', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        username = accounts.query.filter_by(username=username.data).first()
        if username is not None:
            raise ValidationError('Please use a different email address.')
 
    def validate_email(self, email):
        user = accounts.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class TradeForm(FlaskForm):
    ticker_symbol = StringField('Ticker Symbol', validators=[DataRequired()])
    number_of_shares = IntegerField('Number of Shares', validators=[DataRequired()])
    submit = SubmitField('Submit Trade')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class SearchHoldingForm(FlaskForm):
    ticker_symbol = StringField('Ticker Symbol', validators=[DataRequired()])
    submit = SubmitField('Search Holding')

class GetQuote(FlaskForm):
    ticker_symbol = StringField('Ticker Symbol', validators=[DataRequired()])
    submit = SubmitField('Get Quote')

class AssessmentForm(FlaskForm):
    ticker_symbol = StringField('Ticker Symbol', validators=[DataRequired()])
    submit = SubmitField('Get Quote')
