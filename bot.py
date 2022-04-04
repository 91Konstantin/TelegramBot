import config
import idsList #Авторизованные
import telebot
from telebot import types

#Для поиска последнего файла в папке
import os
import time

def CheckFileTime(path, TimeDeltaMax):
    files = os.listdir(path) #Все файлы в директории
    files = [os.path.join(path, file) for file in files] #Превратим просто список файлов в список файлов с путями
    files = [file for file in files if os.path.isfile(file)] #Оставляем в списке только файлы
    MaxTimeFile = max(files, key=os.path.getctime) #Путь к файлу с максимальной датой
    TimeDelta = time.time() - os.path.getmtime(MaxTimeFile) #Вычисляем разницу во времени создания сайта и текущей в секундах
    if TimeDelta > TimeDeltaMax:
        return 1
    else:
        return 0

def GetMaxTimeFilePath(path):
    files = os.listdir(path) #Все файлы в директории
    files = [os.path.join(path, file) for file in files] #Превратим просто список файлов в список файлов с путями
    files = [file for file in files if os.path.isfile(file)] #Оставляем в списке только файлы
    MaxTimeFilePath = max(files, key=os.path.getctime) #Путь к файлу с максимальной датой
    return MaxTimeFilePath

#Для логирования
import logging
from datetime import datetime

logging.basicConfig(filename = config.LogPath, 
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO)
logging.warning('Bot script start')
def LogMessage(message):
    MessageLog = ('Message from {0} {1} (id = {2}) {3}'.format(
    message.from_user.first_name,
    message.from_user.last_name,
    str(message.from_user.id), message.text))
    return MessageLog

#Присваивание токена
bot = telebot.TeleBot(config.TOKEN)

#При старте
@bot.message_handler(commands=['start', 'go'])    
def start_handler(message):
    logging.info(LogMessage(message))
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    btn1 = types.KeyboardButton(text='EOL и кадидаты')
    kb.add(btn1)
    if message.from_user.id not in idsList.ids:
        bot.send_message(message.chat.id, str('ID пользователя НЕ в списке разрешённых. ID:') + str(message.from_user.id))
    else:
        bot.send_message(message.chat.id, str('Авторизован :) Привет, ') + str(message.from_user.first_name) +str('!'), reply_markup=kb)
        

# Ограничение доступа к боту по ID
@bot.message_handler(func=lambda message: message.chat.id not in idsList.ids)
def some(message):
    bot.send_message(message.chat.id, 'Не дозволено общаться с незнакомцами')

# Обработка кнопки 'EOL и кадидаты'
@bot.message_handler(content_types=['text'])
def button_handler(message):
    logging.info(LogMessage(message))
    if message.text == 'EOL и кадидаты':
        bot.send_message(message.chat.id, 'Ушёл считать. Жди:)')
        FileCheck = CheckFileTime(config.EOLPath, config.TimeDeltaMax)
        if FileCheck ==0:
            doc = open(GetMaxTimeFilePath(config.EOLPath), 'rb')
            bot.send_document(message.chat.id, doc)
        if FileCheck ==1:
            bot.send_message(message.chat.id, 'Тут будет функция создания нового файла') #Вставить функцию
            doc = open(GetMaxTimeFilePath(config.EOLPath), 'rb')
            bot.send_document(message.chat.id, doc)
        else:
            pass
    else:
        bot.send_message(message.chat.id, 'Нет такой команды')


#Цикл
bot.polling(none_stop=True)