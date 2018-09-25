import model
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

#temp_var = model.getuserfromkey(7821507)

def api_authenticate(api_key):
    return model.getuserfromkey(api_key)

@app.route('/api/balance/<api_key>', methods=['GET'])
def get_balance(api_key):
    pk, username = api_authenticate(api_key)
    if not pk:
        return jsonify({"ERROR": "BAD API"})
    balance = model.get_balance(pk)
    return jsonify({"balance": balance,
                    "username": username})

@app.route('/api/holdings/<api_key>', methods=['GET'])
def get_holdings(api_key):
    pk, username = api_authenticate(api_key)
    if not pk:
        return jsonify({"ERROR": "BAD API"})
    holdings = model.get_holdings(pk)
    return jsonify(holdings)

@app.route('/api/order_history/<api_key>/<ticker_symbol>', methods=['GET'])
def order_history(api_key, ticker_symbol):
    pk, username = api_authenticate(api_key)
    if not pk:
        return jsonify({"ERROR": "BAD API"})
    order_history = model.get_orders(pk, ticker_symbol)
    return jsonify(order_history)

@app.route('/api/quote/<api_key>/<ticker_symbol>', methods=['GET'])
def quote(api_key, ticker_symbol):
    pk, username = api_authenticate(api_key)
    if not pk:
        return jsonify({"ERROR": "BAD API"})
    quote = model.quote(ticker_symbol)
    return jsonify(quote)

@app.route('/api/buy/<api_key>', methods=['POST'])
def buy(api_key):
    #return str(request.json)
    pk, username = api_authenticate(api_key)
    if not pk:
        return jsonify({"ERROR": "BAD API (BUY)"})
    if not request.json or "symbol" not in request.json or "volume" not in request.json:
        return jsonify({"ERROR" : "BAD REQUEST, MISSING EITHER VOLUME OR SYMBOL(BUY)"})
    ticker_symbol = request.json["symbol"]
    volume = request.json["volume"]
    buy = model.buy(pk, ticker_symbol, volume)
    if not buy:
        return jsonify({"ERROR": "BUY DIDNT WORK"})
    return jsonify({"username": username})

@app.route('/api/sell/<api_key>', methods=['POST'])
def sell(api_key):
    pk, username = api_authenticate(api_key)
    if not pk:
        return jsonify({"ERROR": "BAD API (SELL)"})
    if not request.json or "symbol" not in request.json or "volume" not in request.json:
        return jsonify({"ERROR" : "BAD REQUEST, MISSING EITHER VOLUME OR SYMBOL(SELL)"})
    ticker_symbol = request.json["symbol"]
    volume = request.json["volume"]
    sell = model.sell(pk, ticker_symbol, volume)
    if not sell:
        return jsonify({"ERROR": "SELL DIDNT WORK"})
    return jsonify({"username": username})



if __name__ == "__main__":
    app.run("127.0.0.1",debug=True)