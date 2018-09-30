from app import app, db
from app import model, models
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, TradeForm, TradeType
from flask_login import current_user, login_user, logout_user, login_required
from app.models import accounts, holdings, orders
from werkzeug.urls import url_parse
from random import randint
from datetime import datetime
from wtforms import Form, RadioField
import requests
import json


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html", title='Home', balances=round(get_user_balance(current_user), 2))

@app.route('/holdings', methods=['GET'])
@login_required
def uholdings():
    return render_template("holdings.html", title='Holdings', userholdings=get_holdings(current_user))

@app.route('/orderhistory', methods=['GET'])
@login_required
def orderhistory():
    return render_template("orderhistory.html", title='Order History', orderhistory=get_orders(current_user))

#TODO WORK ON THIS!!!!!
@app.route('/trade', methods=['GET', 'POST'])
@login_required
def trade():
    form = TradeType()
    return render_template("trade.html", title='Trade', form=form, balance=round(get_user_balance(current_user), 2))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        account=accounts.query.filter_by(username=form.username.data).first()
        if account is None or not account.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(account, remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = accounts(username=form.username.data, email=form.email.data, balance=form.balance.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congradulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

def get_user_balance(current_user):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    balances=currentuser.balance
    return balances

def get_holding(current_user, ticker_symbol):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    account_pk=currentuser.id
    holding=holdings.query.filter_by(account_pk=account_pk, ticker_symbol=ticker_symbol).all()
    if holding[0].ticker_symbol == None:
        return None
    else:
        return holding[0].number_of_shares

def get_holdings(current_user):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    account_pk=currentuser.id
    userholdings=holdings.query.filter_by(account_pk=account_pk).all()
    return userholdings

def get_orders(current_user):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    account_pk=currentuser.id
    ordershistory=orders.query.filter_by(account_pk=account_pk).all()
    return ordershistory

def create_holding(current_user, ticker_symbol, number_of_shares, price = 0):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    account_pk=currentuser.id
    new_holding = holdings(ticker_symbol=ticker_symbol, number_of_shares=number_of_shares, account_pk=account_pk)
    db.session.add(new_holding)
    db.session.commit()
    
def modify_holding(current_user, ticker_symbol, new_number_of_shares, price = 0):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    currentholding = holdings.query.filter_by(account_pk=account_pk, ticker_symbol=ticker_symbol).first()
    currentholding.number_of_shares = new_number_of_shares
    db.session.commit()

def modify_balance(current_user, new_amount):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    currentuser.balance = new_amount
    db.session.commit()

def create_order(current_user, ticker_symbol, trade_volume, last_price):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    neworder=orders(ticker_symbol=ticker_symbol, last_price=quote(ticker_symbol), trade_volume=trade_volume, account_pk=account_pk)
    db.session.add(neworder)
    db.session.commit()
    

def buy(current_user, ticker_symbol, number_of_shares):
    holding = get_holding(current_user, ticker_symbol)
    stock_price = quote(ticker_symbol)
    if get_user_balance(current_user) > (stock_price * number_of_shares):
        if holding != None:
            new_number_of_shares = holding + number_of_shares
            modify_holding(current_user, ticker_symbol, new_number_of_shares, 0)
        else:
            create_holding(current_user, ticker_symbol, number_of_shares)
        new_balance = get_user_balance(current_user) - (stock_price * number_of_shares)
        modify_balance(current_user, new_balance)
        create_order(current_user, ticker_symbol, number_of_shares, stock_price)
        return True
    else:
        return False

def sell(current_user, ticker_symbol, number_of_shares):
    number_of_current_shares = get_holding(current_user, ticker_symbol)
    if number_of_current_shares == None:
        return False
    elif number_of_current_shares < number_of_shares:
        return False
    else:
        last_price = quote(ticker_symbol)
        new_number_of_shares = get_holding(current_user, ticker_symbol) - number_of_shares
        modify_holding(current_user, ticker_symbol, new_number_of_shares)
        new_amount = get_user_balance(current_user) + float(number_of_shares * last_price)
        modify_balance(current_user, new_amount)
        sold_number_of_shares = -number_of_shares
        create_order(current_user, ticker_symbol, sold_number_of_shares, last_price)
        return True

def quote(ticker_symbol):
    endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' + ticker_symbol
    response = requests.get(endpoint).text
    try:
        jsondata = json.loads(response)
    except:
        return randint(1,10000) / 100.0
    return json.loads(response)['LastPrice']
