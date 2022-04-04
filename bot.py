import config
import idsList #Авторизованные
import telebot
from telebot import types

#Для вызова данных ЦБ
import GetCBdata

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
    btn1 = types.KeyboardButton(text='ЦБ РФ')
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
    
    if message.text == 'ЦБ РФ':
        try:
            CurString = GetCBdata.GetCurString()
            bot.send_message(message.chat.id, CurString[0])
            bot.send_message(message.chat.id, CurString[1])
            bot.send_message(message.chat.id, CurString[2])
            bot.send_message(message.chat.id, CurString[3])
        except Exception: 
            bot.send_message(message.chat.id,'Что-то пошло не так...')
            logging.info(LogMessage(message) + str(' Fail'))

    #Отправка лога по запросу администратора
    elif (message.chat.id in idsList.Adminids) & (message.text == 'лог'):
        try:
            logging.info(LogMessage(message))
            doc = open(config.LogPath, 'rb')
            bot.send_document(message.chat.id, doc)
        except Exception: 
            bot.send_message(message.chat.id,'Что-то пошло не так...')
            logging.info(LogMessage(message) + str(' Fail'))

    else:
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
        btn1 = types.KeyboardButton(text='ЦБ РФ')
        kb.add(btn1)
        bot.send_message(message.chat.id, 'Нет такой команды', reply_markup=kb)

#Цикл
bot.polling(none_stop=True)