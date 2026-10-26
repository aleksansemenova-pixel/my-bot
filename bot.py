import telebot
from telebot import types
from flask import Flask
from threading import Thread
import random
import os

# ВСТАВЬ СЮДА СВОЙ ТОКЕН ОТ BOTFATHER (вместе с кавычками)
TOKEN = '8955782716:AAFPmurIkqWzx84qT74q4S6gAItcC4WA74k'
bot = telebot.TeleBot(TOKEN)

# Списки для случайных фраз и фактов
greetings = [
    "Привет от секретаря NighttimeBastard.", 
    "Создатель занят, ждите)", 
    "Я на связи. Чего тебе?",
    "Бот на месте. Слушаю."
]

facts = [
    "Коты спят 70% своей жизни.", 
    "У кошек 32 мышцы в каждом ухе.", 
    "Мурлыканье помогает котам восстанавливаться.",
    "Коты не чувствуют сладкий вкус.",
    "Усы помогают котам ориентироваться в пространстве."
]

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, random.choice(greetings))

# Команда /cat (отправляет картинку и случайный факт)
@bot.message_handler(commands=['cat'])
def send_cat(message):
    if os.path.exists('images') and os.listdir('images'):
        random_img = random.choice(os.listdir('images'))
        photo = open(f'images/{random_img}', 'rb')
        bot.send_photo(message.chat.id, photo, caption=random.choice(facts))
    else:
        bot.send_message(message.chat.id, "Ой, картинок пока нет в папке images :(")

# Пасхалка (секретное слово nighttime)
@bot.message_handler(func=lambda message: message.text and message.text.lower() == 'nighttime')
def easter_egg(message):
    bot.send_message(message.chat.id, "🌑 Ты вызвал тьму... Создатель скоро ответит.")

# Команда /menu (кнопки)
@bot.message_handler(commands=['menu'])
def show_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_cat = types.KeyboardButton('🐈 Котик')
    btn_easter = types.KeyboardButton('🌑 Пасхалка')
    markup.add(btn_cat, btn_easter)
    bot.send_message(message.chat.id, "Выбери действие:", reply_markup=markup)

# Обработка нажатий на кнопки
@bot.message_handler(func=lambda message: message.text == '🐈 Котик')
def btn_cat_clicked(message):
    bot.send_message(message.chat.id, "Секунду, ищу котика...", reply_markup=types.ReplyKeyboardRemove())
    send_cat(message)

@bot.message_handler(func=lambda message: message.text == '🌑 Пасхалка')
def btn_easter_clicked(message):
    bot.send_message(message.chat.id, "Вызываю тьму...", reply_markup=types.ReplyKeyboardRemove())
    easter_egg(message)

# Реакция на обычные сообщения
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()
    
    if text.startswith('/'):
        return
        
    if "привет" in text:
        bot.reply_to(message, "И тебе привет, зачем пожаловал?")
    elif "как дела" in text:
        bot.reply_to(message, "А я собираю данные... Шучу. Всё отлично!")
    elif "ты кто" in text:
        bot.reply_to(message, "Я ночной секретарь. Слежу за порядком.")
    elif "код 138" in text:
        bot.reply_to(message, 'Послание от вашего котика: "Я люблю тебя, мой мальчик" ❤️')
    else:
        bot.reply_to(message, "Я тебя услышал, но пока не знаю, что ответить. Напиши /help")

# --- ЗАПУСК БОТА И FLASK ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    keep_alive()
    bot_thread = Thread(target=bot.infinity_polling)
    bot_thread.start()
    print("Бот запущен и слушает сообщения...")
