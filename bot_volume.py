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
emoji_green_circle = '\U0001F7E2'
emoji_red_circle = '\U0001F534'
client = Client(API_KEY,API_SECRET)


def detector_trans():
        
         
                # watchlist = ['ADAUSDT','ADABUSD','ADABTC','ATOMUSDT','AVAXUSDT','BNBUSDT','BTCUSDT','DOTUSDT','ETHUSDT','ETHBTC','ENJUSDT','INJUSDT','LINKUSDT','LUNAUSDT',
                # 'MATICUSDT','MATICBTC','MANAUSDT','STXUSDT','SOLUSDT','SUSHIUSDT','UNIUSDT','WAVESUSDT','XLMUSDT','XLMBTC','ZRXUSDT']
                # for ticker in watchlist:
                        # pair = ticker

                        #Accessing the function of the API-Binance
                symbol = client.get_recent_trades(symbol=('BTCUSDT'),limit=1)
                df = pd.DataFrame(symbol)
                df.drop_duplicates()
                convert_to_dict = df.to_dict()

                # for trans in convert_to_list:
                #         price = trans['qty']
                #         quantity = trans['price']
                #         buy_sell = trans['isBuyerMaker']

                #         total_usd = quantity * price
                print(symbol[[0][1]])
                print(type(symbol))


#                                 #Filter to the transactional volume 
#                                 if total_usd >= 5000 and buy_sell == False:
#                                         update.message.textd(f'''BIG BUY DETECTED {emoji_buy} {emoji_green_circle} 
#                 {ticker}
# Cantidad monedas: {quantity}
# Precio: {price}''' '\n'
# 'Cantidad usd: ' '{0:,.2f}'.format(total_usd))
                                        

#                                 elif total_usd >=  5000 and buy_sell == True:
#                                         update.message.message(f'''BIG SELL DETECTED {emoji_sell} {emoji_red_circle}
#                 {ticker}
# Cantidad en monedas: {quantity}
# Precio: {price}''' '\n'
# 'Cantidad en usd: ' '{0:,.2f}'.format(total_usd))

                                
def run():
        updater = Updater(TOKEN)
        dispatcher = updater.dispatcher

        
        dispatcher.add_handler(CommandHandler('start',detector_trans))


        updater.start_polling()
        updater.idle()


if __name__ == '__main__':   
     detector_trans()
     #for stop the bot, press in console CTRL + C
     

