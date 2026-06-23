import telebot
from telebot import types
import threading
import time

# 🔑 ВСТАВ СВІЙ ТОКЕН ТУТ
bot = telebot.TeleBot("8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q")

user_requests = {}

# ------------------------
# ІМІТАЦІЯ ПЕРЕВІРКИ
# ------------------------
def check_uz(from_city, to_city, date):
    return True  # тест

def check_tickets(from_city, to_city, date):
    return True  # тест

# ------------------------
# МОНІТОРИНГ
# ------------------------
def monitor():
    while True:
        for chat_id, data in user_requests.items():
            try:
                uz = check_uz(data["from"], data["to"], data["date"])
                tickets = check_tickets(data["from"], data["to"], data["date"])

                if uz or tickets:
                    markup = types.InlineKeyboardMarkup()

                    btn1 = types.InlineKeyboardButton(
                        "🚆 Укрзалізниця",
                        url="https://booking.uz.gov.ua"
                    )

                    btn2 = types.InlineKeyboardButton(
                        "🎫 Tickets.ua",
                        url="https://tickets.ua"
                    )

                    markup.add(btn1, btn2)

                    bot.send_message(
                        chat_id,
                        f"🚆 Є квитки!\n{data['from']} → {data['to']}\n📅 {data['date']}",
                        reply_markup=markup
                    )

            except Exception as e:
                print("error:", e)

        time.sleep(30)

# ------------------------
# START
# ------------------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Напиши маршрут:\nКиїв-Чоп-12.07"
    )

# ------------------------
# INPUT
# ------------------------
@bot.message_handler(func=lambda m: True)
def handle(message):
    try:
        text = message.text.replace(" ", "")
        parts = text.split("-")

        if len(parts) != 3:
            bot.send_message(message.chat.id, "Формат: Київ-Чоп-12.07")
            return

        user_requests[message.chat.id] = {
            "from": parts[0],
            "to": parts[1],
            "date": parts[2]
        }

        bot.send_message(message.chat.id, "🔔 Моніторинг увімкнено!")

    except:
        bot.send_message(message.chat.id, "Помилка вводу")

# ------------------------
# START BOT
# ------------------------
threading.Thread(target=monitor, daemon=True).start()
bot.polling(none_stop=True)