import telebot
from telebot import types

TOKEN = "8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q"

bot = telebot.TeleBot(TOKEN)

user_data = {}


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("📅 Дата")
    keyboard.row("⏰ Час")
    keyboard.row("✍️ Ввести вручну")

    bot.send_message(
        message.chat.id,
        "Привіт! Обери дію:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text == "📅 Дата")
def choose_date(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("12.07", "13.07")
    keyboard.row("14.07", "15.07")
    keyboard.row("⬅️ Назад")

    bot.send_message(message.chat.id, "Обери дату:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "⏰ Час")
def choose_time(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("17:00", "20:25")
    keyboard.row("22:30")
    keyboard.row("⬅️ Назад")

    bot.send_message(message.chat.id, "Обери час:", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "✍️ Ввести вручну")
def manual(message):
    msg = bot.send_message(
        message.chat.id,
        "Введи дату або час вручну:"
    )
    bot.register_next_step_handler(msg, save_manual)


def save_manual(message):
    user_data[message.chat.id] = message.text
    bot.send_message(
        message.chat.id,
        f"Збережено: {message.text}"
    )


@bot.message_handler(
    func=lambda message: message.text in [
        "12.07", "13.07", "14.07", "15.07",
        "17:00", "20:25", "22:30"
    ]
)
def save_choice(message):
    user_data[message.chat.id] = message.text
    bot.send_message(
        message.chat.id,
        f"Вибрано: {message.text}"
    )


@bot.message_handler(func=lambda message: message.text == "⬅️ Назад")
def back(message):
    start(message)


@bot.message_handler(func=lambda message: True)
def fallback(message):
    bot.send_message(message.chat.id, "Напиши /start")


print("Bot started")
bot.infinity_polling()
