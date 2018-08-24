import sqlite3
import time
from functools import lru_cache
import requests
import json
from random import randint


connection = sqlite3.connect("example.db")
cursor = connection.cursor()

def quote(ticker_symbol):
    endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol=' + ticker_symbol
    response = requests.get(endpoint).text
    try:
        jsondata = json.loads(response)
    except:
        return randint(1,10000) / 100.0
    return json.loads(response)['LastPrice']

def login(username, password):
    SQL = "SELECT pk FROM accounts WHERE username = ? AND password = ?"
    values = (username, password)
    cursor.execute(SQL, values)
    testvar = cursor.fetchone()
    if testvar == None:
        return None
    else:
        return testvar[0]

def create_user(username, password, balance):
    SQL = """INSERT INTO accounts (username, password, balance) VALUES (?, ?, ?);"""
    values = (username, password, balance)
    cursor.execute(SQL, values)
    connection.commit()

def get_balance(pk):
   
   #connection = sqlite3.connect(‘example.db’, check_same_thread = False)
   #cursor = connection.cursor()
   sql = "SELECT balance FROM accounts WHERE pk = ?"
   cursor.execute(sql, (pk,))
   balance = cursor.fetchone()
   connection.commit()
   if balance == None:
       return None
   else:
       return balance[0]

def get_holdings(pk):
    SQL = "SELECT ticker_symbol, number_of_shares FROM holdings WHERE account_pk = ?"
    values = (pk,)
    cursor.execute(SQL, values)
    testvar2 = cursor.fetchall()
    result = []
    for row in testvar2:
        dic = {
            "ticker_symbol":row[0],
            "number_of_shares":row[1]
        }
        result.append(dic)
    return result


def get_holding(pk, ticker_symbol):
   
   #connection = sqlite3.connect(‘example.db’, check_same_thread = False)
   #cursor = connection.cursor()
   sql = "SELECT number_of_shares FROM holdings WHERE account_pk = ? and ticker_symbol = ?"
   cursor.execute(sql,(pk,ticker_symbol))
   holding = cursor.fetchone()
   connection.commit()
   
   if holding == None:
       return None
   else:
       return holding[0]



def get_orders(pk, ticker_symbol, cutoff=None):
    SQL = '''SELECT ticker_symbol,last_price, trade_volume, timestamp FROM
 orders WHERE account_pk = ? AND ticker_symbol = ?;'''
    values = (pk, ticker_symbol)
    cursor.execute(SQL, values)
    lst = []
    rows = cursor.fetchall()
    for i in rows:
        d = {
        'ticker_symbol': i[0],
        'last_price': i[1],
        'trade_volume': i[2],
        'timestamp': i[3]}
        lst.append(d)
    return lst

def create_holding(account_pk, ticker_symbol, number_of_shares, price = 0):
    SQL = '''INSERT INTO holdings (account_pk, ticker_symbol, number_of_shares)
VALUES (?, ?, ?)'''
    values = (account_pk, ticker_symbol, number_of_shares)
    cursor.execute(SQL, values)


def modify_holding(account_pk, ticker_symbol, number_of_shares, price=0):
    SQL = '''UPDATE holdings SET number_of_shares = ?
WHERE ticker_symbol = ? AND  account_pk = ?'''
    values = (number_of_shares, ticker_symbol, account_pk)
    cursor.execute(SQL, values)
    connection.commit()

def modify_balance(account_pk, new_amount):
    SQL = '''UPDATE accounts SET balance = ? WHERE pk = ?'''
    cursor.execute(SQL,(new_amount, account_pk))
    connection.commit()

def create_order(account_pk, ticker_symbol, trade_volume, last_price):
    SQL = '''INSERT INTO orders (account_pk, ticker_symbol, last_price, trade_volume, timestamp)
            VALUES (?, ?, ?, ?, ?)'''
    values = (account_pk, ticker_symbol, last_price, trade_volume, int(time.time()))
    cursor.execute(SQL,values)
    connection.commit()

def buy(account_pk, ticker_symbol, volume):
   holding = get_holding(account_pk, ticker_symbol)
   stock_price = quote(ticker_symbol)
   if get_balance(account_pk) > (stock_price * volume):
       if holding != None:
           new_holding = holding + volume
           modify_holding(account_pk, ticker_symbol, new_holding, 0)
       else:
           create_holding(account_pk, ticker_symbol, volume)

       new_balance = get_balance(account_pk) - (stock_price *volume)
       modify_balance(account_pk, new_balance)
       create_order(account_pk, ticker_symbol, volume, stock_price)
       return True
   else:
       return False

def sell(account_pk, ticker_symbol, number_of_shares):
    #Does my holding have enough shares?
    number_of_current_shares = get_holding(account_pk, ticker_symbol)
    if number_of_current_shares == None:
        return False
    elif number_of_current_shares < number_of_shares:
        return False
    else:
        #What is the share price?
        last_price = quote(ticker_symbol)
        #Calculate Remaining number of shares
        new_number_of_shares = get_holding(account_pk, ticker_symbol) - number_of_shares
        #Modify our Holdings
        modify_holding(account_pk, ticker_symbol, new_number_of_shares)
        #Modify Balance
        new_amount = get_balance(account_pk) + float(number_of_shares * last_price)
        modify_balance(account_pk, new_amount)
        #sold_number_of_shares = -number_of_shares
        #Create Order
        create_order(account_pk, ticker_symbol, number_of_shares, last_price)
        #Return True
        return True