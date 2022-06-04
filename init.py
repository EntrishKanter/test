import telebot, sqlite3
from telebot import types
from databases import *

bot = telebot.TeleBot(token='5595846062:AAF5f_xvJzNEDw-uxdouT3KRpqxbcQ2ZlK', parse_mode='Markdown')



coins = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width = 1).add(
            types.InlineKeyboardButton("Начать", callback_data="start"))
    bot.send_message(message.chat.id, "*Тест на IQ - точный, онлайн*.\nРезультат прохождения теста на IQ выдается сразу без необходимости в регистрации или СМС. Для начала тестирования кликните выше на кнопку – Начать", reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'start':
        coins[call.from_user.id] = [0, 0]
        markup = types.InlineKeyboardMarkup()
        for button in IQ_test[coins[call.from_user.id][1]]['buttons']:
            markup.add(types.InlineKeyboardButton(button['text'], callback_data=button['callback']))
        bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=IQ_test[coins[call.from_user.id][1]]['text'], reply_markup=markup)
    else:
        coin = coins[call.from_user.id][0] + float(call.data)
        nums = coins[call.from_user.id][1] + 1
        if nums == len(IQ_test):
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=f'Результаты теста: {coins[call.from_user.id][0]}')
        else:
            coins[call.from_user.id] = [coin, nums]
            markup = types.InlineKeyboardMarkup()
            for button in IQ_test[coins[call.from_user.id][1]]['buttons']:
                markup.add(types.InlineKeyboardButton(button['text'], callback_data=button['callback']))
            bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=IQ_test[coins[call.from_user.id][1]]['text'], reply_markup=markup)
            print(coins[call.from_user.id][0])
bot.polling()
