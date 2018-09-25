import sqlite3

with sqlite3.connect("example.db", check_same_thread=False) as c:
    cursor = c.cursor()

    cursor.execute("""
INSERT INTO accounts(username, password, balance)
VALUES("carter", "swordfish", 1000.00)
""")
    cursor.execute("""
INSERT INTO holdings(account_pk, ticker_symbol, number_of_shares)
VALUES(1, "TSLA", 10);
""")
    cursor.execute("""
INSERT INTO holdings(account_pk, ticker_symbol, number_of_shares)
VALUES(1, "AAPL", 10);
""")
    cursor.execute("""
INSERT INTO orders(account_pk, ticker_symbol, last_price, trade_volume,
    timestamp)
VALUES(1, "TSLA", 420.00, 20, 100000)
""")
    cursor.execute("""
INSERT INTO orders(account_pk, ticker_symbol, last_price, trade_volume,
    timestamp)
VALUES(1, "TSLA", 440.00, -10, 150000)
""")
    cursor.execute("""
INSERT INTO orders(account_pk, ticker_symbol, last_price, trade_volume,
    timestamp)
VALUES(1, "AAPL", 208.00, 20, 200000)
""")
    cursor.execute("""
INSERT INTO orders(account_pk, ticker_symbol, last_price, trade_volume,
    timestamp)
VALUES(1, "AAPL", 210.00, -10, 250000)
""")
    c.commit()

#connection = sqlite3.connect('example.db', check_same_thread=False)
#cursor = connection.cursor()
