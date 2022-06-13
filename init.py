from os import sep
import telebot, sqlite3, json
from telebot import types
from googletrans import Translator


bot = telebot.TeleBot(token='5449315934:AAEb8QbG9VMwrNWWgEQDI4v_0xci1LJef_o', parse_mode='Markdown')
translator = Translator()

control_table = {}
coins = {}

@bot.message_handler(commands=['lang'])
def lang(message):
    markup = types.InlineKeyboardMarkup(row_width = 6).add(
        types.InlineKeyboardButton("🇺🇸🇬🇧", callback_data="lang_en"),
        types.InlineKeyboardButton("🇷🇺", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇺🇦", callback_data="lang_uk"),
        types.InlineKeyboardButton("🇯🇵", callback_data="lang_ja"),
        types.InlineKeyboardButton("🇩🇪", callback_data="lang_de"))
    bot.send_message(message.chat.id, 'Choose your language', reply_markup=markup)
@bot.message_handler(commands=['start'])
def start(message):
    connect = sqlite3.connect('data.db')
    cursor = connect.cursor()

    if len(cursor.execute(f"SELECT lang FROM users WHERE id = {message.chat.id}").fetchall()) == 0:
        markup = types.InlineKeyboardMarkup(row_width = 6).add(
            types.InlineKeyboardButton("🇺🇸🇬🇧", callback_data="lang_en"),
            types.InlineKeyboardButton("🇷🇺", callback_data="lang_ru"),
            types.InlineKeyboardButton("🇺🇦", callback_data="lang_uk"),
            types.InlineKeyboardButton("🇯🇵", callback_data="lang_ja"),
            types.InlineKeyboardButton("🇩🇪", callback_data="lang_de"))
        bot.send_message(message.chat.id, 'Choose your language', reply_markup=markup)
    else:
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        markup = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard=True, one_time_keyboard=True)

        for table in tables:
            if table[0] != 'users':
                markup.add(types.KeyboardButton(text=str(table[0])))

        lang = cursor.execute(f"SELECT lang FROM users WHERE id = {message.chat.id}").fetchall()
        bot.send_message(message.chat.id, text=translator.translate(f'Меню теста', dest=lang[0][0]).text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def control_table(message):
    connect = sqlite3.connect('data.db')
    cursor = connect.cursor()
    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for table in tables:
        if table[0] == message.text:
            coins[message.chat.id] = [0, 1, table[0]]
            markup = types.InlineKeyboardMarkup()

            tables = cursor.execute(f"SELECT * FROM '{message.text}' WHERE id = {coins[message.chat.id][1]}").fetchall()
            lang = cursor.execute(f"SELECT lang FROM users WHERE id = {message.chat.id}").fetchall()
            for button in json.loads(tables[0][2]):
                markup.add(types.InlineKeyboardButton(text=str(translator.translate(button['text'], dest=lang[0][0]).text), callback_data=button['callback']))
        
            title = translator.translate(str(tables[0][1]), dest=lang[0][0]).text
            bot.send_message(message.chat.id, text=title, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        connect = sqlite3.connect('data.db')
        cursor = connect.cursor()
        if call.data[:4] == 'lang':
            title = translator.translate('Привет! Я - бот для проверки IQ!\nУ меня есть много тестов на IQ. Тестирование разработано по методики лучших специалистов в области тестирования IQ: Г. Айзенка, К. Рассела, Ф. Картера, Н. Салливана.', dest=str(call.data).split(sep='_')[1]).text
            bot.send_message(call.from_user.id, title)
            if len(cursor.execute(f"SELECT lang FROM users WHERE id = {call.from_user.id}").fetchall()) == 0:
                cursor.execute(f"INSERT INTO users VALUES(?, ?)", (call.from_user.id, str(call.data).split(sep='_')[1]))
            else:
                cursor.execute(f"UPDATE users SET lang = '{str(call.data).split(sep='_')[1]}' WHERE id = {call.from_user.id}")
            connect.commit()


            tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            markup = types.ReplyKeyboardMarkup(row_width = 1, resize_keyboard=True, one_time_keyboard=True)
            for table in tables:
                if table[0] != 'users':
                    markup.add(types.KeyboardButton(text=str(table[0])))
                    
            bot.send_message(call.from_user.id, text=translator.translate(f'Меню теста', dest=str(call.data).split(sep='_')[1]).text, reply_markup=markup)
        else:
            coin = coins[call.from_user.id][0] + float(call.data)
            nums = coins[call.from_user.id][1] + 1
            tab = coins[call.from_user.id][2]
            lang = cursor.execute(f"SELECT lang FROM users WHERE id = {call.from_user.id}").fetchall()
            tables = cursor.execute(f"SELECT * FROM '{tab}' WHERE id = {nums}").fetchall()
            if nums >= len(cursor.execute(f"SELECT * FROM '{tab}'").fetchall()):
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=translator.translate(f'Ваш IQ: {coins[call.from_user.id][0]}\nРасшифровка результата:\nДо 70 баллов -> низкий\nОт 70 до 85 баллов -> ниже среднего\nот 95 до 105 баллов -> средний\nот 105 до 115 баллов -> выше среднего\nот 115 до 130 -> высокий уровень\nот 130 -> около гениальный или гениальный уровень интеллекта\n/start, чтобы пройти другой тест', dest=lang[0][0]).text)
            else:
                coins[call.from_user.id] = [coin, nums, tab]
                markup = types.InlineKeyboardMarkup()
                for button in json.loads(tables[0][2]):
                    markup.add(types.InlineKeyboardButton(text=str(translator.translate(button['text'], dest=lang[0][0]).text), callback_data=button['callback']))
                title = translator.translate(str(tables[0][1]), dest=lang[0][0]).text
                print(title)
                bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.id, text=title, reply_markup=markup)
    except Exception as ex:
        print(ex)


def STARTUP():
    try:
        bot.polling()
    except:
        from time import sleep
        sleep(5)
        STARTUP()

STARTUP()