from telegram.ext import Updater
from telegram.ext import CommandHandler
import logging
from telegram.ext import InlineQueryHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
#from configs import token ### this must be set in the config file. not comitted to github for privacy issues.
from stockapi import StockInfo
import os
### generate updater using token
TOKEN = os.getenv("API_KEY", "optional-default") ## get from heroku environment

PORT = int(os.environ.get('PORT', 5000))

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
updater.bot.setWebhook('https://stonksbot.herokuapp.com/' + TOKEN)

updater.idle()