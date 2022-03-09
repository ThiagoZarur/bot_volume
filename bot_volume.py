from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, dispatcher,CommandHandler
from binance.client import Client, AsyncClient
from decouple import config
import time 
from datetime import datetime
import pytz
import pandas as pd
import asyncio


API_KEY = config('API_KEY', default='')
API_SECRET = config('API_SECRET', default='')
TOKEN = config('TOKEN', default='')

emoji_buy = '\U0001F4C8'
emoji_sell = '\U0001F4C9'
my_city_timezone = pytz.timezone('America/Mexico_City')
my_city_time = datetime.now(my_city_timezone)
client = Client(API_KEY,API_SECRET)


#hacerlo con pandas para al rato
#Crear un vector y filtrar los pares que quieres
#Ver si no se esta almacenando mucha data y eliminarlo
def to_btc(): 

        while True:
                depth = client.get_orderbook_tickers()
                symbol = list(filter(lambda ticker: ticker["symbol"] == 'DOTUSDT',depth))
                # symbol = list(filter(lambda ticker: ticker["symbol"] == "ETHBTC" or ticker["symbol"] == "MATICBTC" or ticker["symbol"] == "ZRXBTC" or ticker["symbol"] == "LINKBTC" or ticker["symbol"] == "ADABTC" or ticker["symbol"] == "XLMBTC" or ticker["symbol"] == "SOLBTC",depth))
                # get_price_bitcoin = client.get_recent_trades(symbol="BTCUSDT")
                # price = get_price_bitcoin[0]
                # convert_price = float(price['price'])

                for ticker in symbol:
                        bidQty = round(float(ticker["bidQty"]),2)
                        askQty =  round(float(ticker["askQty"]),2)
                        bid_price = round(float(ticker["bidPrice"]),8)
                        ask_price = round(float(ticker["askPrice"]),8)
                        print(f'precio de compra {bid_price}, cantidad: {bidQty}, precio de venta: {ask_price}, cantidad: {askQty}')
                        time.sleep(2)
                #       parity = str(ticker["symbol"])
                        # date = my_city_time.strftime('%H:%M:S%')

                        # buy = bidQty * bid_price 
                        # sell = askQty * ask_price 

                        # if buy >= 10:
                        #         update.message.reply_text(f'{emoji_buy} ¡Compra fuerte detectada! simbolo: {parity} precio: {bid_price} Cantidad: {buy} BTC')
                        # elif sell >= 10:
                        #         update.message.reply_text(f'{emoji_sell} ¡Venta fuerte detectada! Simbolo: {parity} Precio: {ask_price} Cantidad: {sell} BTC')


#[{'symbol': 'XLMBTC', 'bidPrice': '0.00000477', 'bidQty': '193941.00000000', 'askPrice': '0.00000478', 'askQty': '32834.00000000'}, 
# {'symbol': 'MATICBTC', 'bidPrice': '0.00003771', 'bidQty': '486.00000000', 'askPrice': '0.00003772', 'askQty': '89.30000000'}, 
# {'symbol': 'SOLBTC', 'bidPrice': '0.00228460', 'bidQty': '0.09000000', 'askPrice': '0.00228540', 'askQty': '1.33000000'}]
#{'id': 1278386240, 'price': '43115.76000000', 'qty': '0.00412000', 'quoteQty': '177.63693120', 'time': 1646288686608, 'isBuyerMaker': False, 'isBestMatch': True}
                                       

def to_usd(update: Updater, context: CallbackContext):
        update.message.reply_text('Hi')
        while True:   
                depth = client.get_orderbook_tickers()
                symbol = list(filter(lambda ticker: ticker["symbol"] == "BTCUSDT" or ticker["symbol"] == "ETHUSDT" or ticker["symbol"] == "MATICUSDT" or ticker["symbol"] == "ZRXUSDT" or ticker["symbol"] == "LINKUSDT" or ticker["symbol"] == "ADAUSDT" or ticker["symbol"] == "XLMUSDT" or ticker["symbol"] == "SOLUSDT",depth))

                for ticker in symbol:
                        bidQty = float(ticker["bidQty"])
                        askQty =  float(ticker["askQty"])
                        bid_price = float(ticker["bidPrice"])
                        ask_price = float(ticker["askPrice"])
                        parity = str(ticker["symbol"])

                        buy = bidQty * bid_price
                        sell = askQty * ask_price

                        if buy >= 500000:
                               update.message.reply_text(f'{emoji_buy} ¡Compra fuerte detectada! simbolo: {parity} precio: {bid_price} Cantidad usd: {buy} usd')
                        elif sell >= 500000:
                                update.message.reply_text(f'{emoji_sell} ¡Venta fuerte detectada! Simbolo: {parity} Precio: {ask_price} Cantidad usd: {sell} usd')


#[{'symbol': 'BTCUSDT', 'bidPrice': '43220.53000000', 'bidQty': '0.04884000', 'askPrice': '43220.54000000', 'askQty': '2.96531000'}]
#[{'symbol': 'MATICUSDT', 'bidPrice': '1.58300000', 'bidQty': '2684.700000600', 'askPrice': '1.58400000', 'askQty': '24627.20000000'}]
#[{'symbol': 'ZRXUSDT', 'bidPrice': '0.56530000', 'bidQty': '484.00000000', 'askPrice': '0.56540000', 'askQty': '1190.00000000'}]

def dot():
                #hacerlo en una función y solo pasarle los argumentos con los tickers que varien 

                btc = client.get_recent_trades(symbol="BTCUSDT",limit=10)
                eth = client.get_recent_trades(symbol="ETHUSDT",limit=10)
                dot = client.get_recent_trades(symbol="DOTUSDT",limit=10)
                matic = client.get_recent_trades(symbol="MATICUSDT",limit=10)
                xlm = client.get_recent_trades(symbol="XLMUSDT",limit=10)
                result_todos = []

                #convirtiendo btc 
                dataframe_btc = pd.DataFrame(btc)
                cantidad_btc = dataframe_btc['qty'].astype(float, errors = 'raise')
                price_btc = dataframe_btc['price'].astype(float, errors = 'raise')
                venta_compra = dataframe_btc['isBuyerMaker']
                result_btc = cantidad_btc * price_btc

                
                #convirtiendo eth
                dataframe_eth = pd.DataFrame(eth)
                cantidad_eth = dataframe_eth['qty'].astype(float, errors = 'raise')
                price_eth = dataframe_eth['price'].astype(float, errors = 'raise')
                result_eth = cantidad_eth * price_eth
        

                #convirtiendo dot
                dataframe_dot = pd.DataFrame(dot)
                cantidad_dot = dataframe_dot['qty'].astype(float, errors = 'raise')
                price_dot = dataframe_dot['price'].astype(float, errors = 'raise')
                result_dot = cantidad_dot * price_dot
               

                #convirtiendo matic
                dataframe_matic = pd.DataFrame(matic)
                cantidad_matic = dataframe_matic['qty'].astype(float, errors = 'raise')
                price_matic = dataframe_matic['price'].astype(float, errors = 'raise')
                result_matic = cantidad_matic * price_matic
                
                
                #convirtiendo xlm
                dataframe_xlm = pd.DataFrame(xlm)
                cantidad_xlm = dataframe_xlm['qty'].astype(float, errors = 'raise')
                price_xlm = dataframe_xlm['price'].astype(float, errors = 'raise')
                result_xlm = cantidad_xlm * price_xlm
                result_todos.append(result_btc,result_eth,result_dot)
                
                if result_btc >= 10000 or result_eth >= 10000 or result_dot >= 10000 or result_matic >= 10000 or result_xlm >= 10000:
                        pass

                

#          id        price         qty      quoteQty           time  isBuyerMaker  isBestMatch
#0  273089589  17.76000000  6.59000000  117.03840000  1646801207900         False         True
#           id        price         qty     quoteQty           time  isBuyerMaker  isBestMatch
# 0  273089594  17.75000000  2.81000000  49.87750000  1646801214410          True         True
def run():
        updater = Updater(TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('BTC',to_btc))
        dispatcher.add_handler(CommandHandler('usd',to_usd))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
     dot() 
     
