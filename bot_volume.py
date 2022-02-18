from __future__ import print_function
from telegram import Update, ParseMode, Poll, InlineKeyboardButton, InlineKeyboardMarkup, replymarkup, update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, dispatcher,CommandHandler
from binance.client import Client
import pandas as pd
import time
from decouple import config



API_KEY = config('API_KEY', default='')
API_SECRET = config('API_SECRET', default='')
TOKEN = config('TOKEN', default='')

client = Client(API_KEY,API_SECRET)


def start():
        update.message.reply_text('Hola')

def run():
        depth = pd.DataFrame(client.get_orderbook_tickers())
        filter = depth[depth.symbol == 'BTCUSDT']
        container = filter[filter.bidQty.int.contains(0.01)]

        to_str = str(container)
        # update.message.reply_text('La transacción es la siguiente: ' + to_str)
        print(to_str)
                
def main():
        updater = Updater(TOKEN)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', start)
        dispatcher.add_handler(start_handler)

        echo_handler = MessageHandler(Filters.text & (~Filters.command), run)
        dispatcher.add_handler(echo_handler)

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
     run() 
