from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
#from configs import token ### this must be set in the config file. not comitted to github for privacy issues.
import os
### generate updater using token
TOKEN = os.environ.get("API_KEY") ## get from heroku environment

PORT = int(os.environ.get('PORT', 5000))

import yfinance as yf
import numpy as np
import pandas as pd

def area_plot(prices, dates, name, chatid ):
    import matplotlib.pyplot as plt
    plt.switch_backend('Agg') 
    fig = plt.figure()
    ax = plt.axes()
    ax.plot(dates, prices)

    import matplotlib.dates as mdates
    myFmt = mdates.DateFormatter('%d %b %y')
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_major_locator(plt.MaxNLocator(6))
    ax.set_xlim(dates[0], dates[-1])

    

    min_date = pd.to_datetime(dates[0]).strftime('%d %b %Y') 
    max_date = pd.to_datetime(dates[-1]).strftime('%d %b %Y') 
    plt.title("$"+ name + " Closing Price from " + min_date + " to " + max_date)

    plt.savefig(str(chatid) + "_" + name + '.png')

    return str(chatid) + "_" + name + '.png'

class StockInfo():
    def __init__(self,ticker, chat_id = "000"):
        if isinstance(ticker, str):
            self.tick = yf.Ticker(ticker)
        else:
            self.tick = yf.Ticker(ticker[0])
            assert self.tick.ticker == ticker[0], "Ticker Name Unknown"
        self.hist = self.tick.history(period="5d")
        self.chat_id = chat_id
    
    def latest_price(self):
        close = round(float(self.hist["Close"][-1]),4)
        latest_date = self.hist.index.values[-1]
        latest_date = pd.to_datetime(latest_date).strftime('%d %b %Y')
        
        return str(close), latest_date
    
    def five_day(self):
        close = [round(float(x),4) for x in self.hist["Close"]]
        latest_dates = self.hist.index.values
        
        return 
    
    def days_past(self, num_days = 30):
        self.hist = self.tick.history(period=str(num_days)+"d")
        close = [round(float(x),4) for x in self.hist["Close"]]
        latest_dates = self.hist.index.values
        return area_plot(close, latest_dates, str(self.tick.ticker), self.chat_id)




if __name__ == "__main__":

    updater = Updater(token=TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    def start(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a stonks bot. Please talk to me!")

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    def get_back_stock(*argss):
        stock_class = StockInfo(*argss)
        closing_price, latest = stock_class.latest_price()
        return "The closing price for " + str(argss[0]) + " on " + latest + " is " + str(closing_price) 


    def stock(update, context):
        ret_text = get_back_stock(context.args[0], update.effective_chat.id)
        context.bot.send_message(chat_id=update.effective_chat.id, text=ret_text)

    stock_handler = CommandHandler('stock', stock)
    dispatcher.add_handler(stock_handler)

    def monthlyret(update, context):
        stock_class = StockInfo(context.args[0], update.effective_chat.id)
        image_file = stock_class.days_past(24)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(image_file, 'rb'))
        os.remove(image_file) ##remove file after sending

    monthlyret_handler = CommandHandler('monthlyret', monthlyret)
    dispatcher.add_handler(monthlyret_handler)


    def inline_stock(update, context):
        query = update.inline_query.query
        if not query:
            return
        results = list()
        results.append(
            InlineQueryResultArticle(
                id=query.upper(),
                title='Latest closing stock price',
                input_message_content=InputTextMessageContent(get_back_stock(query.upper()))
            )
        )
        context.bot.answer_inline_query(update.inline_query.id, results)

    inline_stock_handler = InlineQueryHandler(inline_stock)
    dispatcher.add_handler(inline_stock_handler)


    def unknown(update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    #### START WEBHOOKS below

    updater.start_webhook(listen="0.0.0.0",
                            port=int(PORT),
                            url_path=TOKEN)
    updater.bot.setWebhook('https://mega-stonks-bot.herokuapp.com/' + TOKEN)

    updater.idle()