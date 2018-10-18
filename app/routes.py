from app import app, db
from app import models
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, TradeForm, SearchHoldingForm, GetQuote, AssessmentForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import accounts, holdings, orders
from werkzeug.urls import url_parse
from random import randint
from datetime import datetime
from wtforms import Form, RadioField
import requests
import json
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.email import send_password_reset_email

@app.route('/')
@app.route('/index')
@login_required
def index():
    #PUT SOMETHING INTERESTING HERE
    return render_template("index.html", title='Home', balances=round(get_user_balance(current_user), 2))

@app.route('/orderconf')
@login_required
def orderconf():
    return render_template("orderconf.html", title='Order Confirmation')

@app.route('/assessment', methods=['GET', 'POST'])
@login_required
def assessment():
    form = AssessmentForm()
    if form.validate_on_submit():
        ticker_symbol = form.ticker_symbol.data
        return redirect('/assess_result/{}'.format(ticker_symbol))
    return render_template("assessment.html", title='Assessment', form=form)

@app.route('/assess_result/<ticker_symbol>', methods=['GET', 'POST'])
@login_required
def assess_result(ticker_symbol):
    current_holding_shares = get_holding(current_user=current_user, ticker_symbol=ticker_symbol)
    tran_history = get_specific_orders(current_user=current_user, ticker_symbol=ticker_symbol)
    current_price = quote(ticker_symbol)
    if current_holding_shares:
        current_value = current_price * current_holding_shares
    else:
        current_value = 0
    return render_template("assess_result.html", title="Assessment Result", current_holding_shares = current_holding_shares, tran_history = tran_history, current_price = current_price, current_value = current_value, ticker_symbol = ticker_symbol)


@app.route('/pricequote', methods=['GET', 'POST'])
@login_required
def pricequote():
    form = GetQuote()
    if form.validate_on_submit():
        ticker_symbol=form.ticker_symbol.data
        return redirect('/pricequoteresult/{}'.format(ticker_symbol))
    return render_template("pricequote.html", title='Price Quote', form = form)

@app.route('/pricequoteresult/<ticker_symbol>', methods=['GET','POST'])
@login_required
def pricequoteresult(ticker_symbol):
    quote_result=quote(ticker_symbol)
    return render_template("pricequoteresult.html", title='Quote Result', quote_result=round(quote_result, 2), ticker_symbol=ticker_symbol)

@app.route('/holdings', methods=['GET'])
@login_required
def uholdings():
    return render_template("holdings.html", title='Holdings', userholdings=get_holdings(current_user))

@app.route('/specificholdingsearch', methods=['GET', 'POST'])
@login_required
def specificholding():
    form = SearchHoldingForm()
    if form.validate_on_submit():
        ticker_symbol=form.ticker_symbol.data
        return redirect('/specificholdingresult/{}'.format(ticker_symbol))
    return render_template("specificholdingsearch.html", title='Search Holdings', form = form)

@app.route('/specificholdingresult/<ticker_symbol>', methods = ['GET', 'POST'])
@login_required
def holdings_specific(ticker_symbol):
    current_holding_shares = get_holding(current_user=current_user, ticker_symbol=ticker_symbol)
    return render_template("specificholdingresult.html", title='Specific Holding Result', number_of_shares=current_holding_shares, ticker_symbol=ticker_symbol)


@app.route('/orderhistory', methods=['GET'])
@login_required
def orderhistory():
    return render_template("orderhistory.html", title='Order History', orderhistory=get_orders(current_user))

@app.route('/buy', methods=['GET', 'POST'])
@login_required
def buy():
    form = TradeForm()
    if form.validate_on_submit():
        user_buy = buy_stock(current_user=current_user, ticker_symbol=form.ticker_symbol.data, number_of_shares=form.number_of_shares.data)
        if user_buy == True:
            flash('Your order was successful!')
            return redirect(url_for('orderconf'))
        elif user_buy == False:
            flash('Something is wrong. Try again!')
    return render_template("buy.html", title='Buy Stock', form=form, balance=round(get_user_balance(current_user), 2))

@app.route('/sell', methods=['GET', 'POST'])
@login_required
def sell():
    form = TradeForm()
    if form.validate_on_submit():
        user_sell = sell_stock(current_user=current_user, ticker_symbol=form.ticker_symbol.data, number_of_shares=form.number_of_shares.data)
        if user_sell == True:
            flash('Your order was successful!')
            return redirect(url_for('orderconf'))
        elif user_sell == False:
            flash('Something is wrong. Try again!')
    return render_template("sell.html", title='Sell Stock', form=form, userholdings=get_holdings(current_user))

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

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = accounts.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html', title='Reset Password', form=form)

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

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = accounts.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

def get_user_balance(current_user):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    balances=currentuser.balance
    return balances

def get_holding(current_user, ticker_symbol):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    account_pk=currentuser.id
    holding=holdings.query.filter_by(account_pk=account_pk, ticker_symbol=ticker_symbol).all()
    if holding:
        return holding[0].number_of_shares
    else:
        return None

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

def get_specific_orders(current_user, ticker_symbol):
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    account_pk = currentuser.id
    specificorderhistory = orders.query.filter_by(account_pk=account_pk, ticker_symbol=ticker_symbol).all()
    if specificorderhistory:
        return specificorderhistory
    else:
        return None

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
    

def buy_stock(current_user, ticker_symbol, number_of_shares):
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

def sell_stock(current_user, ticker_symbol, number_of_shares):
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
