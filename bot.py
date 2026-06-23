import telebot
from telebot import types

TOKEN = "8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q"
bot = telebot.TeleBot(TOKEN)

user_data = {}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("12.07", "13.07")
    keyboard.row("14.07", "15.07")

    bot.send_message(
        message.chat.id,
        "Привіт! Обери дату:",
        reply_markup=keyboard
    )


# універсальний хендлер
@bot.message_handler(func=lambda message: True)
def handler(message):
    chat_id = message.chat.id
    text = message.text

    if chat_id not in user_data:
        user_data[chat_id] = {}

    # ---------------- DATE ----------------
    if text in ["12.07", "13.07", "14.07", "15.07"]:
        user_data[chat_id]["date"] = text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row("17:00", "20:25")
        keyboard.row("22:30")

        bot.send_message(
            chat_id,
            f"Дата обрана: {text}\nТепер обери час:",
            reply_markup=keyboard
        )
        return

    # ---------------- TIME ----------------
    if text in ["17:00", "20:25", "22:30"]:
        user_data[chat_id]["time"] = text

        date = user_data[chat_id].get("date")

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row("Підтвердити", "Скасувати")

        bot.send_message(
            chat_id,
            f"Перевір:\nДата: {date}\nЧас: {text}",
            reply_markup=keyboard
        )
        return

    # ---------------- CONFIRM ----------------
    if text == "Підтвердити":
        data = user_data.get(chat_id, {})

        bot.send_message(
            chat_id,
            f"✅ Заброньовано!\nДата: {data.get('date')}\nЧас: {data.get('time')}",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return

    # ---------------- CANCEL ----------------
    if text == "Скасувати":
        user_data.pop(chat_id, None)

        bot.send_message(
            chat_id,
            "❌ Скасовано. Натисни /start щоб почати знову.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        return


print("Bot started...")
bot.infinity_polling()
