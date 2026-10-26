import telebot
from flask import Flask
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
    # Проверяем, есть ли папка images и есть ли в ней файлы
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

# Реакция на обычные сообщения
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()
    
    if "привет" in text:
        bot.reply_to(message, "И тебе привет, зачем пожаловал?.")
    elif "как дела" in text:
        bot.reply_to(message, "А я собираю данные... Шучу. Всё отлично!")
    elif "ты кто" in text:
        bot.reply_to(message, "Я ночной секретарь. Слежу за порядком.")
    elif "код 138" in text:
        bot.reply_to(message, 'Послание от вашего котика: "Я люблю тебя, мой мальчик" ❤️')
    else:
        bot.reply_to(message, "Я тебя услышал, но пока не знаю, что ответить. Напиши /help")

# Запуск бота
from threading import Thread

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