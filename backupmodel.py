import sqlite3

connection = sqlite3.connect("example.db")
cursor = connection.cursor()

def login(username, password):
    SQL = "SELECT pk FROM accounts WHERE username = ? AND password = ?"
    values = (username, password)
    cursor.execute(SQL, values)
    #pk_int = "SELECT pk FROM accounts"
    #cursor.execute(pk_int)
    testvar = cursor.fetchone()
    if testvar == None:
        return False
    else:
        return testvar[0]

def get_holdings(pk):
    SQL = "SELECT ticker_symbol, number_of_shares FROM holdings WHERE account_pk = ?"
    values = (pk,)
    cursor.execute(SQL, values)
    testvar2 = cursor.fetchall()
    result = []
    for row in testvar2:
        dic = {
            "Ticker Symbol":row[0],
            "Number of Shares":row[1]
        }
        result.append(dic)
    return result

#print(get_holdings(1))

def get_balance(pk):
    SQL = "SELECT balance FROM accounts WHERE pk = ?"
    values = (pk,)
    cursor.execute(SQL,values)
    testvar = cursor.fetchone()
    if testvar == None:
        return("Wrong Account Number")
    else:
        return testvar[0]

#print(get_balance(1))

def get_holdings_shares(pk, ticker_symbol):
    SQL = "SELECT number_of_shares FROM holdings WHERE account_pk = ? AND ticker_symbol = ?"
    values = (pk, ticker_symbol)
    cursor.execute(SQL, values)
    testvar = cursor.fetchone()
    if testvar == None:
        return None
    else:
        return testvar[0]

#print(get_holdings_shares(1,"NFLX"))


def get_orders(pk, ticker_symbol, cutoff=None):
    SQL = "SELECT timestamp, trade_volume, last_price, ticker_symbol FROM orders WHERE account_pk = ? AND ticker_symbol = ?"
    values = (pk, ticker_symbol)
    cursor.execute(SQL, values)
    testvar = cursor.fetchall()
    result = []
    for row in testvar:
        dic = {
            "ticker_symbol":row[3],
            "timestamp":row[0],
            "trade_volume":row[1],
            "last_price":row[2]
        }
        result.append(dic)
    return result

#print(get_orders(1,"AAPL"))
