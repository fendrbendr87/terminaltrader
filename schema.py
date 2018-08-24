import sqlite3

connection = sqlite3.connect('example.db',check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE accounts(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR,
        password VARCHAR,
        balance FLOAT
    );"""
)

cursor.execute(
    """CREATE TABLE holdings(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        account_pk INTEGER,
        ticker_symbol VARCHAR,
        number_of_shares INTEGER,
        volume_weighted_average_price FLOAT
    );"""
)

cursor.execute(
    """CREATE TABLE orders(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        account_pk INTEGER,
        ticker_symbol VARCHAR,
        last_price FLOAT,
        trade_volume INTEGER,
        timestamp INTEGER
    );"""
)
