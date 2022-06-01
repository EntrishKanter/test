from email import message
from telebot import types 
import telebot
import data
import text
import threading
import time
from flask import Flask

app = Flask(__name__)


bot = telebot.TeleBot(data.API_TOKEN)


def later_hour(user_id):
    time.sleep(10)
    data.SETDATA("schemes",user_id, "scheme_2")
    markup = types.InlineKeyboardMarkup(row_width = 1)
    for button in text.scheme2['buttons']:
        markup.add(types.InlineKeyboardButton(button['text'], callback_data=button['callback']))
    bot.send_message(user_id, text.scheme2['text_2'])
    bot.send_message(user_id, text.scheme2['text_3'], reply_markup=markup)



@bot.message_handler(commands=['start'])
def start(message):
    try:
        if data.IS_VALID("refer_base", message.text[7:]):
            if (data.IS_VALID("user", message.chat.id)):
                bot.send_message(message.chat.id, "Вы уже присоединились")
            else:
                DATA = data.GETDATA("refer_base")
                data.SETDATA("user", message.chat.id, message.chat.id)
                data.SETDATA("refer_base", message.text[7:], int(DATA[message.text[7:]])+1)
                if (int(DATA[message.text[7:]])+1) == 10:
                    bot.send_message(message.text[7:], text.start['text_finish'])
                    bot.send_message(message.text[7:], text.scheme2['text_1'])
                    threading.Thread(target=later_hour, args=[str(message.text[7:])]).start()
                else:
                    bot.send_message(message.text[7:], f"Друг {int(DATA[message.text[7:]])+1} присоединился")
    except:
        pass
    data.SETDATA("user", message.chat.id, message.chat.id)
    markup = types.InlineKeyboardMarkup(row_width = 1)
    for button in text.start['buttons']:
        markup.add(types.InlineKeyboardButton(button['text'], callback_data=button['callback']))
    data.SETDATA("schemes",message.chat.id, "scheme_1")
    bot.send_message(message.chat.id, text.start['text_1'])
    bot.send_message(message.chat.id, text.start['text_2'], reply_markup=markup)









@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    DATA = data.GETDATA("schemes")
    if DATA[str(call.from_user.id)] == "scheme_1":
        if call.data == "buy":
            data.SETDATA('SHOP', call.from_user.id, 'FALSE')
            bot.send_message(call.from_user.id, f"http://176.119.147/184:5000/{call.from_user.id}")
        elif call.data == "free":
            bot.send_message(call.from_user.id, f"{text.start['text_free_1']} t.me/TESTF2Bot?start={call.from_user.id}")
            bot.send_message(call.from_user.id, text.start['text_free_2'])
            data.SETDATA("refer_base",call.from_user.id, 0)
    if DATA[str(call.from_user.id)] == "scheme_2":
        if call.data == "buy":
            bot.send_message(call.from_user.id, "buy")
        elif call.data == "free":
            bot.send_message(call.from_user.id, text.scheme2['text_free'])

@app.route('/<name>')
def index(name):
    bot.send_message(name, text.start['text_finish'])
    bot.send_message(name, text.scheme2['text_1'])
    threading.Thread(target=later_hour, args=[str(name)]).start()
    return "Paid"


def StartUpApp():
    app.run(host='0.0.0.0', port=47747)
def StartUpBot():
    bot.polling()

if __name__ == '__main__':
    threading.Thread(target=StartUpBot).start()
    threading.Thread(target=StartUpApp).start()