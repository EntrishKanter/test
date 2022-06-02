import threading
from telebot import types
from flask import Flask
import files, telebot, data, time

bot = telebot.TeleBot(token=data.API_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    photo = open('photo/photo_1.png', 'rb')
    bot.send_message(message.chat.id, "аы раыораыар орыо ароыроар \nhttps://imgv3.fotor.com/images/homepage-feature-card/Fotor-AI-photo-enhancement-tool-ru.jpg")
    # bot.send_photo(message.chat.id, [open('photo/photo_1.png', 'rb'),caption='желаемый текст');

bot.polling()