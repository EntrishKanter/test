from pickle import FALSE, TRUE
import threading
from telebot import types
from flask import Flask
import files, telebot, data, time

bot = telebot.TeleBot(token=data.API_TOKEN)
app = Flask(__name__)


def send_scheme(user_id, number_scheme, type):
    DATA_SCHEME = files.GETDATA('schemes')
    if type == True:
        time.sleep(int(DATA_SCHEME[number_scheme]['sleep']))
    markup = types.InlineKeyboardMarkup(row_width = 1)
    for button in DATA_SCHEME[number_scheme]['buttons']:
        markup.add(types.InlineKeyboardButton(button['text'], callback_data=button['callback']))
    try:
        bot.send_photo(user_id, photo=open(DATA_SCHEME[number_scheme]['photo'], 'rb'))
    except:
        pass
    bot.send_message(user_id, DATA_SCHEME[number_scheme]['text'], reply_markup=markup)
@bot.message_handler(commands=['start'])
def start(message):
    try:
        if files.IS_VALID('ref_user',str(message.text[7:]).split(sep="u")[0]):
            if files.IS_VALID('users', message.chat.id):
                bot.send_message(message.chat.id, "Вы уже здесь")
            else:
                DATA_SCHEME = files.GETDATA("schemes")[str(message.text[7:]).split(sep="u")[1]]
                for permission in DATA_SCHEME['permissions']:
                    if permission == "free":
                        DATA_REF = str(files.GETDATA("ref_user")[str(message.text[7:]).split(sep="u")[0]]).split(sep="&")
                        if int(DATA_SCHEME['permissions']['free']) == int(DATA_REF[0])+1:
                            bot.send_message(str(message.text[7:]).split(sep="u")[0], DATA_SCHEME["free"])
                            threading.Thread(target=send_scheme, args=[message.chat.id, "scheme_2", True]).start()
                        else:
                            files.SETDATA("ref_user", str(message.text[7:]).split(sep="u")[0], f"{int(DATA_REF[0])+1}&{DATA_REF[1]}")
                            bot.send_message(str(message.text[7:]).split(sep="u")[0], f"Друг {int(DATA_REF[0])+1} присоединился")
    except:
        pass
    if not(files.IS_VALID('users', message.chat.id)):
        files.SETDATA('users', message.chat.id, f'scheme_1&user')
    send_scheme(message.chat.id, "scheme_1", False)


@bot.message_handler(commands=['repost'])
def repost(message):
    DATA_USER = files.GETDATA('users')
    def reposting(message):
        for usr in DATA_USER:
            try:
                time.sleep(0.04)
                threading.Thread(target=send_scheme, args=[usr, message.text, False]).start()
            except:
                pass
    for usr in DATA_USER:
        if (str(usr) == str(message.chat.id)) and (str(DATA_USER[usr]).split(sep="&")[1] == "admin"):
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            for scheme in files.GETDATA('schemes'):
                markup.add(types.KeyboardButton(text=scheme))
            msg = bot.send_message(message.chat.id, "Схемы:", reply_markup=markup)
            bot.register_next_step_handler(msg, reposting)








@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    DATA_SCHEME = files.GETDATA('schemes')
    for data in DATA_SCHEME[str(call.data).split(sep="&")[1]]['buttons']:
        if call.data == data['callback']:
            files.SETDATA('ref_user', call.from_user.id, f"0&{call.data}")
            amount = DATA_SCHEME[str(call.data).split(sep="&")[1]]['amount']
            url = f"https://global24.pro/wid/c2w/?lang=ru&callbackUrl=http//:127.0.0.1:5000/{str(call.from_user.id)}/scheme_2&cardAmount={amount}&quittanceDest=my@mail.com&email=my@mail.com&walletId=12345678901234&blocked=1&type=c2w"
            ref_url = f't.me/TESTF2Bot?start={call.from_user.id}u{str(call.data).split(sep="&")[1]}'
            bot.send_message(call.from_user.id, str(data["reposnce"]).replace('{{url}}', url).replace('{{ref_url}}', ref_url))


@app.route('/<name>/<scheme>')
def index(name, scheme):
    if files.IS_VALID("users",name):
        if files.IS_VALID("schemes", scheme):
            DATA_SCHEMES = files.GETDATA("schemes")[scheme]
            bot.send_message(str(name), DATA_SCHEMES["paid"])
            if scheme == 'scheme_1':
                threading.Thread(target=send_scheme, args=[name, "scheme_2", True]).start()
    return "PAID"




def StartUpApp():
    app.run(host=data.IP_HOST, port=data.IP_PORT)
def StartUpBot():
    bot.polling()

if __name__ == '__main__':
    threading.Thread(target=StartUpBot).start()
    threading.Thread(target=StartUpApp).start()