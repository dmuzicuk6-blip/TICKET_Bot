import telebot
from telebot import types

TOKEN = "8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("17:00", "20:25")
    keyboard.row("22:30", "Ввести свій час")

    bot.send_message(
        message.chat.id,
        "Привіт! Обери час:",
        reply_markup=keyboard
    )

@bot.message_handler(func=lambda message: True)
def handle(message):
    if message.text == "Ввести свій час":
        bot.send_message(message.chat.id, "Напиши час вручну (наприклад 18:45)")
    else:
        bot.send_message(message.chat.id, f"Ти вибрала: {message.text}")

print("Bot started")
print("Bot started")
bot.infinity_polling()
