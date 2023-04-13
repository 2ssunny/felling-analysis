from copyreg import dispatch_table
import telegram
from telegram.ext import Updater
from telegram.ext import Filters
from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
import random

import config
import list


token = config.token
id = config.id

bot = telegram.Bot(token)
bot.sendMessage(chat_id=id, text="반갑습니다. ''/start' 입력해 실행하세요")

updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
updater.start_polling()


def cmd_task_buttons(update, context):
    task_buttons = [[
        InlineKeyboardButton('1.설명', callback_data=1), InlineKeyboardButton(
            '2.명언', callback_data=2), InlineKeyboardButton('3.감정입력', callback_data=3)
    ], [
        InlineKeyboardButton('4.감정점수', callback_data=4), InlineKeyboardButton(
            '5.분석', callback_data=5), InlineKeyboardButton('6.예측', callback_data=6)
    ], [
        InlineKeyboardButton('7.종료', callback_data=7)
    ]]

    reply_markup = InlineKeyboardMarkup(task_buttons)

    context.bot.send_message(
        chat_id=update.message.chat_id, text='실행할 옵션을 선택해주세요.', reply_markup=reply_markup
    )


def cb_button(update, context):
    query = update.callback_query
    data = query.data

    context.bot.send_chat_action(
        chat_id=update.effective_user.id, action=ChatAction.TYPING
    )

    if data == '7':
        context.bot.edit_message_text(
            text='작업이 종료되었습니다.', chat_id=query.message.chat_id, message_id=query.message.message_id
        )
    else:
        # context.bot.edit_message_text(
        #     text='[{}] 작업이 진행중입니다.'.format( data )
        #     , chat_id=query.message.chat_id
        #     , message_id=query.message.message_id
        # )

        if data == '1':
            context.bot.send_message(chat_id=id, text=list.help_return)
        elif data == '2':
            context.bot.send_message(
                chat_id=id, text=random.choice(list.phrase_list))
        elif data == '3':
            print("감정입력")
        elif data == '4':
            print("감정점수")
        elif data == '5':
            print("분석")
        elif data == '6':
            print("예측")

        context.bot.send_message(
            chat_id=update.effective_chat.id, text="다른작업을 선택하려면 ''/again'을 입력하세요".format(
                data)
        )


task_buttons_handler = CommandHandler(['start', 'again'], cmd_task_buttons)
# task_buttons_handler = CommandHandler( 'again', cmd_task_buttons )
button_callback_handler = CallbackQueryHandler(cb_button)

dispatcher.add_handler(task_buttons_handler)
dispatcher.add_handler(button_callback_handler)

updater.start_polling()
updater.idle()
