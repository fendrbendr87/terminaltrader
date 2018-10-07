from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from time import time
from app import login, app
import jwt


class accounts(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    balance=db.Column(db.Float)
    api_key=db.Column(db.Integer)
    holdings=db.relationship('holdings', backref='positions', lazy='dynamic')
    orders=db.relationship('orders', backref='order_history', lazy='dynamic')

    def __repr__(self):
        return '<accounts {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
        {'reset_password': self.id, 'exp': time() + expires_in},
        app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class holdings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker_symbol=db.Column(db.String(20))
    number_of_shares=db.Column(db.Integer)
    volume_weighted_average_price=db.Column(db.Float)
    account_pk=db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __repr__(self):
        return '<holdings> ticker_symbol: {}, number_of_shares: {}, VWAP: {}'.format(self.ticker_symbol, self.number_of_shares, self.volume_weighted_average_price)


class orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker_symbol=db.Column(db.String(20))
    last_price=db.Column(db.Float)
    trade_volume=db.Column(db.Integer)
    timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    account_pk=db.Column(db.Integer, db.ForeignKey('accounts.id'))

    def __repr__(self):
        return '<orders> ticker: {}, last price: {}, volume: {}, time: {}'.format(self.ticker_symbol, self.last_price, self.trade_volume, self.timestamp)

@login.user_loader
def load_user(id):
    return accounts.query.get(int(id))