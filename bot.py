import telebot
from telebot import types
import os

TOKEN = os.getenv("8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q")

# перевірка токена (щоб не падало)
if not TOKEN:
    raise Exception("BOT_TOKEN not found in environment variables")

bot = telebot.TeleBot(TOKEN)

user_data = {}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("📅 Дата", "⏰ Час")
    markup.add("✍️ Ввести вручну")

    bot.send_message(message.chat.id, "Вибери дію:", reply_markup=markup)


# дата
@bot.message_handler(func=lambda m: m.text == "📅 Дата")
def date(message):
    bot.send_message(message.chat.id, "📅 Доступні варіанти: сьогодні / будь-яка дата")


# меню часу
@bot.message_handler(func=lambda m: m.text == "⏰ Час")
def time_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add("17:00", "20:25", "22:30")
    markup.add("⬅️ Назад")

    bot.send_message(message.chat.id, "Оберіть час:", reply_markup=markup)


# вибір часу
@bot.message_handler(func=lambda m: m.text in ["17:00", "20:25", "22:30"])
def choose_time(message):
    user_data[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"✔️ Обрано: {message.text}")


# ручний ввід
@bot.message_handler(func=lambda m: m.text == "✍️ Ввести вручну")
def manual(message):
    msg = bot.send_message(message.chat.id, "Введи час (наприклад 18:45):")
    bot.register_next_step_handler(msg, save_manual)


def save_manual(message):
    user_data[message.chat.id] = message.text
    bot.send_message(message.chat.id, f"✔️ Збережено: {message.text}")


# назад
@bot.message_handler(func=lambda m: m.text == "⬅️ Назад")
def back(message):
    start(message)


# захист від крашу
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "Натисни /start")


print("Bot started...")
bot.polling(none_stop=True)
