from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, dispatcher,CommandHandler
from binance.client import Client
from decouple import config
import time 
from datetime import datetime
import pytz
import pandas as pd


API_KEY = config('API_KEY', default='')
API_SECRET = config('API_SECRET', default='')
TOKEN = config('TOKEN', default='')

emoji_buy = '\U0001F4C8'
emoji_sell = '\U0001F4C9'
my_city_timezone = pytz.timezone('America/Mexico_City')
my_city_time = datetime.now(my_city_timezone)
client = Client(API_KEY,API_SECRET)


def detector_trans():
        
                tickers = ['BTCUSDT', 'ETHUSDT','MATICUSDT','ZRXUSDT','DOTUSDT','XLMUSDT']
                for ticker in tickers:
                        pair = ticker

                        symbol = client.get_recent_trades(symbol=(pair),limit=1)        
                        for trans in symbol:
                                quantity = float(trans['qty'])
                                price = float(trans['price'])
                                buy_sell = bool(trans['isBuyerMaker'])
                                total_usd = quantity * price

                                if total_usd >= 1000 and buy_sell == False:
                                        print(f'''Moneda: {pair}
BIG BUY DETECTED {emoji_buy}
Cantidad en monedas: {quantity}
Precio: {price}
Cantidad en usd: {total_usd}''')

                                elif total_usd >= 1000 and buy_sell == True:
                                        print(f'''Moneda: {pair}
BIG SELL DETECTED {emoji_sell}
Cantidad en monedas: {quantity}
Precio: {price}
Cantidad en usd: {total_usd}''')

                                
def run():
        updater = Updater(TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start',detector_trans))
        # dispatcher.add_handler(CommandHandler('usd',to_usd))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':   
     detector_trans()
     

