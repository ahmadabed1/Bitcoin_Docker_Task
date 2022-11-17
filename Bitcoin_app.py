from flask import Flask
import requests
import redis

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def getCurrnetBitCoinPrice(): 
    BitCoin_Current_Price = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD').json()['USD']
    return BitCoin_Current_Price

def getAverageBitCoinPrice():
    
    BitCoin_EveryMinute_Price = requests.get('https://min-api.cryptocompare.com/data/v2/histominute?fsym=BTC&tsym=USD&limit=9').json()['Data']['Data']
    sum=0
    for everyminute in BitCoin_EveryMinute_Price:
        # everyminute['close'] its the price for minute
        sum+=everyminute['close']
    return (sum/10)

@app.route("/")
def home():

    while True:
        price = float("{:.4f}".format(getCurrnetBitCoinPrice()))
        average_price = float("{:.4f}".format(getAverageBitCoinPrice()))
        # save it in redis
        cache.set('currentPrice', price)
        cache.set('averagePrice', average_price)

        return """
        <meta http-equiv="refresh" content="1" /><h1>Current BitCoin Price is: {}$</h1><br> <h1>Average BitCoin Price Last 10 Minutes: 
        {}$ </h1>""".format(price,average_price)

