from app import app, db
from app import model, models
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import accounts, holdings, orders
from werkzeug.urls import url_parse



@app.route('/')
@app.route('/index')
@login_required
def index():
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    account_pk=currentuser.id
    userholdings=holdings.query.filter_by(account_pk=account_pk).all()
    orderhistory=orders.query.filter_by(account_pk=account_pk).all()
    return render_template("index.html", title='Home', userholdings=userholdings, balances=get_user_balance(current_user), orderhistory=orderhistory)

#TODO WORK ON THIS!!!!!
@app.route('/trade', methods=['GET', 'POST'])
@login_required
def trade():
    currentuser = accounts.query.filter_by(username=current_user.username).first()
    balances=currentuser.balance
    tickersymbol
    numberofshares
    return render_template("trade.html", title='Trade', balances=balances, tickersymbol=tickersymbol, numberofshares=numberofshares)


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
    return render_template('login.html', title='Sign In', form=form), account_pk

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
    balances=current_user.balance
    return balances

