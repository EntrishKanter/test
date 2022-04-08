import telebot
import pytesseract
from PIL import Image


#API 
bot = telebot.TeleBot('5128329216:AAGxHJzTRCR0iq6OPt0Ze_F7PHO0nerfRh0') 
seting = False
problem = '(x > 1) or (x < 10)'


def get_text(text):
    number = ''
    for latter in text:
        try:
            #если число отрицательное
            if latter == '-':
                number = number + '-'
            elif latter == ',' or latter == '.':
                number = number + '.'
            else:
                number = number + str(int(latter))
        except:
            pass
    return number


@bot.message_handler(commands=['setprob'])
def setproblem(message):
    global seting
    seting = True
    def setproblem(message):
        global problem, seting
        problem = message.text
        bot.send_message(message.chat.id, 'Готово')
        seting = False
    msg = bot.send_message(message.chat.id, f'Ваше условие: \n\nСейчас: {problem}\n\nПримеры: (x > 1) or (x < 10)')
    bot.register_next_step_handler(msg, setproblem)


@bot.message_handler(content_types=['text'])
def text(message):
    if not(seting):
        try:     
            number = int(message.text) 
        except:
            number = get_text(message.text)
        problem_ = problem.replace('x', str(number))
        print(problem_)
	try:
        	if eval(problem_) == True:
            		bot.send_message(message.chat.id, 'True')
	except:
		pass


@bot.message_handler(content_types=['photo'])
def photo(message):
    photo_id = message.photo[-1].file_id
    photo_file = bot.get_file(photo_id) # <class 'telebot.types.File'>
    photo_bytes = bot.download_file(photo_file.file_path) # <class 'bytes'>
    with open(r't.png', "wb") as new_file:
        new_file.write(photo_bytes)
    img = Image.open(r"t.png")
    number = get_text(pytesseract.image_to_string(img))
    problem_ = problem.replace('x', str(number))
    print(problem_)
    try:
    	if eval(problem_) == True:
        	bot.send_message(message.chat.id, 'True')
    except:
	pass


bot.polling() # запускаем бота