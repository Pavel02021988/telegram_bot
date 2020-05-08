from telegram import Bot
from telegram import Update
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from config import token
from db import init_db
from db import count_messages
from db import add_message
from db import list_messages

command_count = 'count'
command_list = 'list'

def get_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='кол-во сообщений',
                                                                       callback_data=command_count)],
                                                 [InlineKeyboardButton(text='мои сообщения',
                                                                      callback_data=command_list)]])

def message_handler(update, context):
    user = update.effective_user
    if user:
        name = user.first_name
    else:
        name = 'anonim'
    text = update.effective_message.text
    reply_text = f'hello, {name}\n\n{text}'
    update.message.reply_text(text=reply_text, reply_markup=get_keyboard())
    if text:
        add_message(user_id=user.id, text=text)

def callback_handler(update, context):
    user = update.effective_user
    callback_data = update.callback_query.data
    if callback_data == command_count:
        count = count_messages(user_id=user.id)
        text = f'у Вас {count} сообщений'
    elif callback_data == command_list:
        messages = list_messages(user_id=user.id, limit=5)
        text = '\n'.join([f'#{message_id}-{message_text}' for message_id, message_text in messages])

    else:
        text = 'произошла ошибка'
    update.effective_message.reply_text(text=text)

def main():
    bot = Bot(token=token, base_url="https://telegg.ru/orig/bot")
    updater = Updater(bot=bot, use_context=True)
    init_db()
    updater.dispatcher.add_handler(MessageHandler(Filters.all, message_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()