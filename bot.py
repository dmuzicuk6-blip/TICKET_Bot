import telebot
from telebot import types
import os

bot = telebot.TeleBot(os.getenv("8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q"))

user_data = {}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    btn1 = types.KeyboardButton("📅 Обрати дату")
    btn2 = types.KeyboardButton("⏰ Обрати час")
    btn3 = types.KeyboardButton("✍️ Ввести вручну")

    markup.add(btn1, btn2)
    markup.add(btn3)

    bot.send_message(message.chat.id, "Привіт! Обери дію:", reply_markup=markup)


# дата
@bot.message_handler(func=lambda m: m.text == "📅 Обрати дату")
def date(message):
    bot.send_message(message.chat.id, "Вибір дати: сьогодні / будь-яка дата")


# час кнопки
@bot.message_handler(func=lambda m: m.text == "⏰ Обрати час")
def time_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("17:00", "20:25", "22:30")
    markup.add("⬅️ Назад")

    bot.send_message(message.chat.id, "Оберіть час:", reply_markup=markup)


# ручний ввід
@bot.message_handler(func=lambda m: m.text == "✍️ Ввести вручну")
def manual(message):
    msg = bot.send_message(message.chat.id, "Введи свій час (наприклад 18:45):")
    bot.register_next_step_handler(msg, save_manual_time)


def save_manual_time(message):
    user_data[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"Збережено час: {message.text}")


# вибір часу кнопками
@bot.message_handler(func=lambda m: m.text in ["17:00", "20:25", "22:30"])
def select_time(message):
    user_data[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"Вибрано час: {message.text}")


# назад
@bot.message_handler(func=lambda m: m.text == "⬅️ Назад")
def back(message):
    start(message)


bot.polling()
