import time
from datetime import datetime

def login_option():
    print("BEFORE WE GET STARTED, WOULD YOU LIKE TO: ")
    print("1) LOGIN")
    print("2) CREATE AN ACCOUNT")
    selection = input("WHICH OPTION DO YOU CHOOSE? ")
    return selection

def create_account():
    username = input("USERNAME: ")
    password = input("PASSWORD: ")
    balance = float(input("INITIAL DEPOSIT: "))
    return username, password, balance

def login_prompt(error = False):
    if error:
        print("LOGIN INCORRECT!!")
    username = input("USERNAME: ")
    password = input("PASSWORD: ")
    return username, password

def welcome():
    print("WELCOME TO TERMINAL TRADER!")

def main_menu():
    print("MAIN MENU")
    print("OPTIONS:")
    print("1) ACCOUNT BALANCE AND HOLDINGS")
    print("2) BUY STOCK")
    print("3) SELL STOCK")
    print("4) ORDER HISTORY")
    print("5) QUOTE")
    print("6) GET USER API_KEY")
    print("0) EXIT")
    print()
    selection = input("WHICH OPTION DO YOU CHOOSE? ")
    return selection

def pause():
    input("OKAY?")
    print("\n\n\n\n\n")

def failuremessage():
    print("YOU DONT GOT ENOUGH MONEY!\n\n\n")
    pause()

def successmessage():
    print("GOOD JOB!\n\n\n")
    pause()

def getsymbol():
    symb = str(input("Please input your ticker symbol: "))
    return symb

def volume():
    volume = float(input("Please input the number of shares: "))
    return volume

def quote_prompt():
    ticker_symbol = input("Which ticker symbol do you want to see the price? ")
    return ticker_symbol

def show_key(api_key):
    print("YOUR API_KEY IS: ", api_key)

def display_quote(ticker_symbol,quote):
    print("The quote for {} is {}.".format(ticker_symbol,quote))

def show_status(balance, holdings):
    print("{0:^40}".format("BALANCE:"))
    print("{0:^40}".format(balance),"\n")
    print("{0:^40}".format("HOLDINGS:"))
    print("{0:^20}{1:^20}\n".format("TICKER SYMBOL","NUMBER OF SHARES"))
    for holding in holdings:
        print("{0:^20}".format(holding["ticker_symbol"]), end='')
        print("{0:^20}".format(holding["number_of_shares"]), end='\n')

def sell_menu():
    print('What would you like to sell?')
    ticker_symbol = input()
    print(ticker_symbol)
    print('How much of {} would you like to sell?'.format(ticker_symbol))
    number_of_shares = int(input())
    print(number_of_shares)
    return (ticker_symbol, number_of_shares)


def sell_error():
    print('Sorry, you don\'t have enough shares.')
    print('Would you like to choose another option?')
    print()
    print()

def sell_good():
    print('Sale complete.')


def ticker_request():
    ticker = str(input("PLEASE ENTER THE TICKER SYMBOL YOU WANT TO SEE ORDER HISTORY FOR: "))
    return ticker

def display_order_hist(account_pk, ticker_symbol, orders):
    print("{0:^48}".format("ORDER HISTORY FOR "),end='')
    print(ticker_symbol)
    print("\n\n")
    print("{0:^16}{1:^16}{2:^16}\n".format("TIME STAMP", "TRADE VOLUME", "LAST_PRICE"))
    for stocks in orders:
        print("{0:^16}".format(datetime.utcfromtimestamp(stocks["timestamp"]).strftime('%Y-%m-%d %H:%M:%S')),end='')
        print("{0:^16}".format(stocks["trade_volume"]),end='')
        print("{0:^16}".format(stocks["last_price"]),end='\n')
    print("\n\n")
