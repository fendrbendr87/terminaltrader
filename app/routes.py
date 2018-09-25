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
    #holdings="testing"
    holding = accounts.query.filter_by(username=str(current_user)).first()
    holdings = holding.email
    #holdings = model.get_balance(current_user.id)
    return render_template("index.html", title='Home', holdings=holdings)


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
        user = accounts(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congradulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

