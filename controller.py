import model
import view

if __name__ == "__main__":
    pk = None
    #THIS IS WHERE WE HAVE LOGIN OPTION()
    view.welcome()
    #THIS IS WHERE WE STORE USER'S CHOICE
    initial_option = view.login_option()
    first_exit_terminal = False
    while first_exit_terminal == False:
        if initial_option.strip() == "2":
            username, password, balance = view.create_account()
            model.create_user(username, password, balance)
            print("USER SUCCESSFULLY CREATED, PLEASE RELOG")
            first_exit_terminal == True
            exit()
        elif initial_option.strip() == "1":
            #THIS IS WHAT USER SEES AFTER OPTION 1
            view.welcome()
            username, password = view.login_prompt()
            pk = model.login(username, password)
            while pk == None:
                username, password = view.login_prompt(True)
                pk = model.login(username, password)
            exit_terminal = False
            while exit_terminal == False:
                option = view.main_menu()
                if option.strip() == "0":
                    exit_terminal = True
                    exit()
                elif option.strip() == "1":
                    balance = model.get_balance(pk)
                    holdings = model.get_holdings(pk)
                    view.show_status(balance, holdings)
                    view.pause()
                elif option.strip() == "2":
                    account_pk = pk
                    ticker_symbol = view.getsymbol()
                    number_of_shares = view.volume()
                    #float(volume)
                    finalbuy = model.buy(account_pk, ticker_symbol,number_of_shares)
                    if finalbuy == False:
                        view.failuremessage()
                    else:
                        view.successmessage()
                elif option.strip() == '3':
                    ticker_symbol, number_of_shares = view.sell_menu()
                    status = model.sell(pk, ticker_symbol, number_of_shares)
                    if status == False:
                        view.sell_error()
                    else:
                        view.sell_good()
                elif option.strip() == "4":
                    account_pk = pk
                    ticker_symbol = view.ticker_request()
                    orders = model.get_orders(account_pk, ticker_symbol)
                    view.display_order_hist(account_pk, ticker_symbol,orders)
                elif option.strip() == '5':
                    ticker_symbol = view.quote_prompt()
                    quote = model.quote(ticker_symbol)
                    view.display_quote(ticker_symbol, quote)
                    view.pause()