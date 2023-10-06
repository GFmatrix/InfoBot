#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging
import os
import glob

from handlers import *

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


global get_review
get_review = False

ADMINS = [965758821]

def start(update: Update, context: CallbackContext) -> None:
    get_review = False
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Biz haqimizda", callback_data='Biz haqimizda'),
            InlineKeyboardButton("Yangiliklar", callback_data='Yangiliklar'),
        ],
        [
          InlineKeyboardButton("Aloqa", callback_data='Telefon nomer'),
          InlineKeyboardButton("Fikr bildirish", callback_data='Fikr bildirish'),
        ],
        [
          InlineKeyboardButton("FAQ", callback_data='FAQ'),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    
    query = update.callback_query

    query.answer()
    
    faq = []
    path = os.path.join('FAQ', '*.txt')
    for key, q in enumerate(glob.glob(str(path))):
      
      head, tail = os.path.split(q)
      faq.append(tail[:-4])
      
    if query.data == 'Biz haqimizda':
      query.edit_message_text(text=f"Biz NONAME Tashkilotmiz")
      
    
    elif query.data == 'Yangiliklar':
      mes_id = (query.edit_message_text(text=f"Yangiliklar")).message_id
      for key, news in enumerate(get_news()):
        query.bot.send_photo(chat_id=query.message.chat_id, photo=news['img'], caption=news['title'], reply_markup=news_keyboard(mes_id+key+1, news['link']))
    
    
    if query.data == 'Telefon nomer':
      query.edit_message_text(text=f"Telefon nomer: +998912345678")
    
    
    elif query.data == 'Fikr bildirish':
      query.edit_message_text(text=f"Fikr bildiring:")
    
    
    elif query.data == 'FAQ':
      keyboard = []
      
      print(str(path))
      for key, faq in enumerate(glob.glob(str(path))):
        head, tail = os.path.split(faq)
        keyboard.append([InlineKeyboardButton(tail[:-4], callback_data=tail[:-4])])
      
      query.edit_message_text(text=f"FAQ:", reply_markup=InlineKeyboardMarkup(keyboard))
      
    elif len(list(filter(lambda x: x in query.data, faq))) > 0:
      with open(os.path.join('FAQ', query.data+'.txt'), 'r') as f:
        query.edit_message_text(text=f.read())
    
    elif len(query.data.split('*')) > 1:
      com = {'b': 'Yomon', 'g': 'Yaxshi', 's': 'Zo\'r'}
      data = query.data.split('*')
      capt = json.loads(os.path.join('data', 'news.json'))
      i = 0
      
      for key, news in enumerate(capt):
        if capt[key]['link'].endswith(data[2]): 
          i = key
          
      query.bot.edit_message_caption(caption=f"{capt[i]['title']}\n{com[data[0]]}", chat_id=query.message.chat_id, message_id=int(data[1]))
    
    # query.edit_message_text(text=f"Selected option: {query.data}")

def get_send_review(update: Update, context: CallbackContext) -> None:
  review = update.message.text
  update.bot.send_message(chat_id=update.message.chat_id, text=f"Fikringiz uchun rahmat!")
  for admin in ADMINS:
    update.bot.send_message(chat_id=admin, text=f"Yangi fikr kelib tushdi: {review}")
    
  
  start(update, context)

def about_us(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    
    

def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("6527372080:AAEcF_9xlU6FG_R2e4Imyd2cPT0QkqL0x3o")


    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # updater.dispatcher.add_handler(MessageHandler(get_send_review))
    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()