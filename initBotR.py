



import telebot, pytesseract
from PIL import Image
from telebot import types 

####################################################
#VALUE
####################################################

MODE_ID, MODE = False, False
bot = telebot.TeleBot('5272793248:AAGrzLdalPEdhZNDRXRit_Hp5MIix7lPFmA') 
problems, current_problem = [], 'x > 0'


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
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
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
    def COMMANDS(message):
        if message.text == 'к работе':
            global MODE
            menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            for problem in problems:
                menu.add(types.KeyboardButton(text=f"set {problem}"))
            menu.add(types.KeyboardButton(text='ID'))
            bot.send_message(message.chat.id, 'Принятие чисел, фото и документов', reply_markup=menu)
            MODE = False
        elif message.text == 'добавить':
            def add(message):
                global problems, current_problem
                if len(problems) == 0:
                    current_problem = message.text.lower()
                problems.append(message.text.lower())
                bot.send_message(message.chat.id, f'Добавлено условие {message.text.lower()}')
                MENU(message)
            msg = bot.send_message(message.chat.id, 'Новое условие')
            bot.register_next_step_handler(msg, add)
        elif message.text == 'удалить':
            menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
            for problem in problems:
                menu.add(types.KeyboardButton(text=problem))
            def remove(message):
                global problems
                problems.remove(message.text)
                bot.send_message(message.chat.id, f'Удалено {message.text}')
                MENU(message)
            msg = bot.send_message(message.chat.id, 'Выберете условия для удаления', reply_markup=menu)
            bot.register_next_step_handler(msg, remove)
        else:
            MENU(message)
    MODE = True
    if len(problems) == 0:
        menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton(text='добавить'))
    else:
        menu = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True).add(
            types.KeyboardButton(text='к работе'),
            types.KeyboardButton(text='добавить'),
            types.KeyboardButton(text='удалить')
        )
    msg = bot.send_message(message.chat.id, 'Меню', reply_markup=menu)
    bot.register_next_step_handler(msg, COMMANDS)



####################################################
#ANSWER
####################################################

@bot.message_handler(content_types=['text'])
def TEXT(message):
    global current_problem
    if not(MODE):
        if get_set(message.text) == 'set ':
            current_problem = message.text[4:]
        elif message.text == 'ID':
            global MODE_ID
            if MODE_ID == True:
                MODE_ID = False
            else:
                MODE_ID = True
        else:
            solution = current_problem.replace('x', GetText(str(message.text)))
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
                solution = current_problem.replace('x', number)
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
                solution = current_problem.replace('x', number)
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


####################################################
#END
####################################################
bot.polling()
