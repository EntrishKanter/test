import telebot, json, datetime, time, threading
from telebot import types
from datetime import datetime as dt


bot = telebot.TeleBot(token='5503954313:AAFgc1y5lKXk2PTXHBYfYhAOSm2xT2slq2U')


posts = {}
photos = []
empty = {}

def sending(name):
    try:
        time.sleep(1)
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("Связаться с менеджером", url="t.me/PZTAbot?start=1"),
            types.InlineKeyboardButton("Перейти на сайт", url="https://www.pzta.ru/")
            )
        while True:
            if dt.fromisoformat(posts[name][1]) < datetime.datetime.now():
                if len(posts[name][0]) == 2:
                    bot.send_photo('-1001782853824', posts[name][0][0], caption=posts[name][0][1], reply_markup=markup)
                    pass
                elif len(posts[name][0]) == 1:
                    bot.send_message('-1001782853824', posts[name][0][0], reply_markup=markup)
                    pass
                else:
                    try:
                        bot.send_media_group('-1001782853824', posts[name][0])
                        pass
                    except Exception as ex:
                        print(ex)
                break
        posts.pop(name)
    except Exception as ex:
        print(ex)


def edit_time(message, name):
    try:
        date_ = dt.fromisoformat(message.text)
        print(posts)
        posts[name] = [posts[name][0], str(date_), True]
        print(posts)
        bot.send_message(message.chat.id, 'Готово', reply_markup=types.ReplyKeyboardRemove())
    except:
        msg = bot.send_message(message.chat.id, 'Неправильный формат, попробуйте ещё раз!')
        bot.register_next_step_handler(msg, edit_time, name)

def reedit_1(message, name):
    if message.text == 'Редактировать время':
        msg = bot.send_message(
            message.chat.id, f'Дата постинга. Пример {datetime.datetime.now()}, можно без секунд, пример, 2022-06-06 18:26')
        bot.register_next_step_handler(msg, edit_time, name)
    if message.text == 'Удалить':
        bot.send_message(message.chat.id, 'Удалено', reply_markup=types.ReplyKeyboardRemove())
        posts.pop(name)
    else:
        bot.send_message(message.chat.id, "Отмена", reply_markup=types.ReplyKeyboardRemove())

def reedit(message):
    if message.text == 'Отмена':
        bot.send_message(message.chat.id, "Вы вышли из меню", reply_markup=types.ReplyKeyboardRemove())
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
            types.KeyboardButton('Редактировать время'),
            types.KeyboardButton('Удалить'))
        if len(posts[message.text][0]) == 2:
            msg = bot.send_photo(message.chat.id, posts[message.text][0][0], caption=posts[message.text][0][1], reply_markup=markup)
            bot.register_next_step_handler(msg, reedit_1, message.text)
        elif len(posts[message.text][0]) == 1:
            msg = bot.send_message(message.chat.id, posts[message.text][0][0], reply_markup=markup)
            bot.register_next_step_handler(msg, reedit_1, message.text)
        else:
            try:
                bot.send_media_group(message.chat.id, posts[message.text][0])
                msg = bot.send_message(message.chat.id, "Управление", reply_markup=markup)
                bot.register_next_step_handler(msg, reedit_1, message.text)
            except Exception as ex:
                print(ex)

@bot.message_handler(commands=['menu'])
def menu(message):
    if int(message.chat.id) == 1600287606:
        print(message.chat.id)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(types.KeyboardButton("Отмена"))
        for data in posts:
            markup.add(types.KeyboardButton(data))
        msg = bot.send_message(message.chat.id, "Ваши посты", reply_markup=markup)
        bot.register_next_step_handler(msg, reedit)

def set_post(message, name):
    if message.text == 'готово':
        threading.Thread(target=sending, args=[name]).start()
        bot.send_message(message.chat.id, "Готово")
    else:
        bot.send_message(message.chat.id, "Отмена")
        posts.pop(name)

def set_data(message, name):
    try:
        date_ = dt.fromisoformat(message.text)
        posts[name] = [posts[name], message.text, True]
        if len(posts[name][0]) == 2:
            bot.send_photo(message.chat.id, posts[name][0][0], caption=posts[name][0][1])
        elif len(posts[name][0]) == 1:
            bot.send_message(message.chat.id, str(posts[name][0][0]))
        else:
            bot.send_media_group(message.chat.id, posts[name][0])
        bot.send_message(message.chat.id, f"Дата постинга: {date_}")
        msg = bot.send_message(message.chat.id, "Напишите слово 'готово'")
        bot.register_next_step_handler(msg, set_post, name)
    except Exception as ex:
        print(ex)
        msg = bot.send_message(message.chat.id, 'Неправильный формат, попробуйте ещё раз!')
        bot.register_next_step_handler(msg, set_data, name)

def set_name(message, value):
    name = f"{message.text} {datetime.datetime.now()}"
    posts[name] = value
    msg = bot.send_message(message.chat.id, f'Дата постинга. Пример {datetime.datetime.now()}, можно без секунд, пример, 2022-06-06 18:26')
    bot.register_next_step_handler(msg, set_data, name)


@bot.message_handler(content_types=['photo'])
def photo(message):
    if int(message.chat.id) == 1600287606:
        if message.media_group_id == None:
            bot.send_photo(message.chat.id,message.photo[0].file_id, caption=message.caption)
            msg = bot.send_message(message.chat.id, 'Название для поста')
            bot.register_next_step_handler(msg, set_name, [message.photo[0].file_id, message.caption])
        else:
            try:
                photos = []
                for ph in empty[message.chat.id]:
                    photos.append(ph)
                photos.append(types.InputMediaPhoto(message.photo[0].file_id))
                empty[message.chat.id] = photos
            except:
                def send_photos(message):
                    time.sleep(3)
                    bot.send_media_group(message.chat.id, empty[message.chat.id])
                    msg = bot.send_message(message.chat.id, 'Название для поста')
                    bot.register_next_step_handler(msg, set_name, empty[message.chat.id])
                empty[message.chat.id] = [types.InputMediaPhoto(message.photo[0].file_id, caption=message.caption)]
                threading.Thread(target=send_photos, args=[message]).start()


@bot.message_handler(content_types=['text'])
def text(message):
    print(message.chat.id)
    if int(message.chat.id) == 1600287606:
        bot.send_message(message.chat.id, message.text)
        msg = bot.send_message(message.chat.id, 'Название для поста')
        bot.register_next_step_handler(msg, set_name, [message.text])


def STARTBOT():
    bot.infinity_polling(timeout=10, long_polling_timeout = 5)
if __name__ == '__main__':
    STARTBOT()

