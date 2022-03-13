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


def detector_trans(update:Updater,context:CallbackContext):
        while True:
                #List of watchlist
                tickers = ['BTCUSDT', 'ETHUSDT','MATICUSDT','ADAUSDT','DOTUSDT','XLMUSDT','ZRXUSDT','LINKUSDT','SOLUSDT','MANAUSDT','SUSHIUSDT','UNIUSDT']
                for ticker in tickers:
                        pair = ticker

                        #Accessing the function of the API-Binance
                        symbol = client.get_recent_trades(symbol=(pair),limit=1)        
                        for trans in symbol:
                                quantity = float(trans['qty'])
                                price = float(trans['price'])
                                buy_sell = bool(trans['isBuyerMaker'])
                                total_usd = quantity * price

                                #Filter to the transactional volume 
                                if total_usd >= 1000000 and buy_sell == False:
                                        update.message.reply_text(f'''Moneda: {pair}
BIG BUY DETECTED {emoji_buy}
Cantidad en monedas: {quantity}
Precio: {price}
Cantidad en usd: {total_usd}''')
                                        #Remove variables so as not to accumulate data
                                        del(pair)
                                        

                                elif total_usd >=  1000000 and buy_sell == True:
                                        update.message.reply_text(f'''Moneda: {pair}
BIG SELL DETECTED {emoji_sell}
Cantidad en monedas: {quantity}
Precio: {price}
Cantidad en usd: {total_usd}''')
                                        #Remove variables so as not to accumulate data
                                        del(pair)

                                
def run():
        updater = Updater(TOKEN)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start',detector_trans))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':   
     run()
     #for stop the bot, press in console CTRL + C
     

