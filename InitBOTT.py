


import telebot, pytesseract
from PIL import Image
from telebot import types 

####################################################
#VALUE
####################################################

MODE_ID, MODE = False, False
bot = telebot.TeleBot('5242165763:AAHJzd4_fm8lEonVRhU316SQ-AoHrytITZ8') 
problems, current_problem = [], 'x > 0'
current_ID = 'x > 0'

####################################################
#DEF 
####################################################



IMAGE = 't.png'
def GetText(text):
    number = ''
    for latter in text:
        try:
            if latter == '-':
                number = number + '-'
            elif latter == ',' or latter == '.':
                number = number + '.'
            elif str(type(int(latter))) == "<class 'int'>":
                number = number + latter
        except:
            pass
    return number
def TextFromImageID():
    Picture = Image.open(IMAGE)
    txt, x, result = pytesseract.image_to_string(Picture).split(sep=' '), 0, []
    while x < len(txt):
        if txt[x] == '©':
            result.append(GetText(str(txt[x+1])))
        x += 1
    return result
def TextFromImage():
    Picture = Image.open(IMAGE)
    result = GetText(pytesseract.image_to_string(Picture))
    return result
def get_set(text):
    try:
        return text[:4]
    except:
        return False




####################################################
#MENU
####################################################
@bot.message_handler(commands=['menu', 'start'])
def MENU(message):
    global MODE
    menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(
        types.KeyboardButton(text='Условия'),
        types.KeyboardButton(text='ID'))


    def CommandsChoose(message):
        if message.text == 'Условия':
            def COMP(message):
                if message.text == 'К работе':
                    global current_problem, MODE
                    MODE = False
                    menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=False)
                    for problem in problems:
                        menu.add(types.KeyboardButton(text=f"set {problem}"))
                    bot.send_message(message.chat.id, f'К работе', reply_markup=menu)
                elif message.text == 'Добавить':
                    def add(message):
                        global problems, current_problem
                        if len(problems) == 0: current_problem = message.text.lower()
                        problems.append(message.text.lower())
                        menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton(text='К работе'),
                            types.KeyboardButton(text='Добавить'),
                            types.KeyboardButton(text='Удалить'))
                        bot.send_message(message.chat.id, f'Добавлено условие {message.text.lower()}', reply_markup=menu)
                        bot.register_next_step_handler(msg, COMP)
                    msg = bot.send_message(message.chat.id, 'Напишите условие:')
                    bot.register_next_step_handler(msg, add)
                elif message.text == 'Удалить':
                    def remove(message):
                        problems.remove(message.text)
                        menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
                        if len(problems) == 0:
                            menu.add(types.KeyboardButton(text='Добавить'))
                        else:
                            menu.add(types.KeyboardButton(text='К работе'),
                                types.KeyboardButton(text='Добавить'),
                                types.KeyboardButton(text='Удалить'))
                        msg = bot.send_message(message.chat.id, f'Удалено {message.text}', reply_markup=menu)
                        bot.register_next_step_handler(msg, COMP)
                    menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
                    for problem in problems: menu.add(types.KeyboardButton(text=problem))    
                    msg = bot.send_message(message.chat.id, 'Выберете условия для удаления', reply_markup=menu)
                    bot.register_next_step_handler(msg, remove)
                else:
                    MENU(message)
            menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            if len(problems) == 0:
                menu.add(types.KeyboardButton(text='Добавить'))
            else:
                menu.add(types.KeyboardButton(text='К работе'),
                    types.KeyboardButton(text='Добавить'),
                    types.KeyboardButton(text='Удалить'))
            msg = bot.send_message(message.chat.id, 'Управление для условий', reply_markup=menu)
            bot.register_next_step_handler(msg, COMP)
        elif message.text == 'ID':
            def ID(message):
                if message.text == 'Установить условие':
                    def add_ID(message):
                        global current_ID
                        current_ID = message.text
                        menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(
                            types.KeyboardButton(text='Установить условие'),
                            types.KeyboardButton(text='К работе'))
                        msg = bot.send_message(message.chat.id, 'Готово', reply_markup=menu)
                        bot.register_next_step_handler(msg, ID)
                    msg = bot.send_message(message.chat.id, 'Новое условие:')
                    bot.register_next_step_handler(msg, add_ID)
                elif message.text == 'К работе':
                    global MODE, MODE_ID
                    menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(
                        types.KeyboardButton('Выкл. ID')
                    )
                    MODE, MODE_ID = False, True
                    bot.send_message(message.chat.id, 'К работе!', reply_markup=menu)
                else:
                    MENU(message)
            menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(
                types.KeyboardButton(text='Установить условие'),
                types.KeyboardButton(text='К работе'))
            msg = bot.send_message(message.chat.id, 'Управление ID', reply_markup=menu)
            bot.register_next_step_handler(msg, ID)
        else:
            MENU(message)
    MODE = True
    msg = bot.send_message(message.chat.id, 'меню', reply_markup=menu)
    bot.register_next_step_handler(msg, CommandsChoose)

@bot.message_handler(content_types=['text'])
def straight(message):
    global MODE_ID, current_problem
    if message.text == 'Выкл. ID':
        MODE_ID = False
        MENU(message)
    elif get_set(message.text) == 'set ':
        current_problem = message.text[4:]
    else:
        if not(MODE):
            if message.text[:4] == 'set ':
                current_problem = message.text[4:]
                bot.send_message(message.chat.id, f'установлено {message.text[4:]}')
            else:
                number = GetText(message.text)
                solution = current_problem.replace('x', number)
                try:
                    print(solution)
                    if eval(solution) == True:
                        bot.send_message(message.chat.id, 'True')
                except:
                    pass


@bot.message_handler(content_types=['document'])
def document(message):
    if not(MODE):
        document_bytes = bot.download_file(bot.get_file(message.document.file_id).file_path) # <class 'bytes'>
        with open(IMAGE, "wb") as new_file:
            new_file.write(document_bytes)
        if MODE_ID == True:  
            result = False
            for number in TextFromImageID():
                solution = current_ID.replace('x', number)
                try:
                    print(solution)
                    if eval(solution) == True:
                        result = True
                except:
                    pass
            if result == True:
                bot.send_message(message.chat.id, result)
        else:
            number = TextFromImage()
            problem_ = current_problem.replace('x', str(number))
            print(problem_)
            try:
                if eval(problem_) == True:
                    bot.send_message(message.chat.id, 'True')
            except:
                pass
 

@bot.message_handler(content_types=['photo'])
def photo(message):
    if not(MODE):
        photo_bytes = bot.download_file(bot.get_file(message.photo[-1].file_id).file_path) # <class 'bytes'>
        with open(r't.png', "wb") as new_file:
            new_file.write(photo_bytes)
        print(TextFromImage())
        if MODE_ID == True:
            result = False
            for number in TextFromImageID():
                solution = current_ID.replace('x', number)
                try:
                    print(solution)
                    if eval(solution) == True:
                        result = True
                except:
                    pass
            if result == True:
                bot.send_message(message.chat.id, result)
        else:
            number = TextFromImage()
            problem_ = current_problem.replace('x', str(number))
            print(problem_)
            try:
                if eval(problem_) == True:
                    bot.send_message(message.chat.id, 'True')
            except:
                pass




bot.polling()