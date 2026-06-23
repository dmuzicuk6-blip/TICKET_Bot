import telebot
from telebot import types
import requests
import time
import threading

TOKEN = "8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q"
bot = telebot.TeleBot(TOKEN)

# збереження запитів
tracking = {}

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привіт 👋\nНапиши маршрут у форматі:\n\nКиїв - Чоп\n12.07\n\nЯ додам моніторинг 🔔"
    )

# ---------------- INPUT ----------------
@bot.message_handler(func=lambda m: "-" in m.text)
def add_tracking(message):
    chat_id = message.chat.id
    lines = message.text.split("\n")

    try:
        route = lines[0]
        date = lines[1]

        from_city, to_city = [x.strip() for x in route.split("-")]

        tracking[chat_id] = {
            "from": from_city,
            "to": to_city,
            "date": date,
            "active": True
        }

        bot.send_message(
            chat_id,
            f"🔔 Моніторинг увімкнено\n\n🚉 {from_city} → {to_city}\n📅 {date}"
        )

    except:
        bot.send_message(chat_id, "❌ Формат неправильний. Напиши:\nКиїв - Чоп\n12.07")


# ---------------- CHECK FUNCTION ----------------
def check_tickets(from_city, to_city, date):
    """
    Тут має бути реальний запит.
    УЗ не має відкритого API, тому це заглушка.
    """

    # Імітація перевірки
    # (сюди можна підключати парсинг сторінки)
    return False


# ---------------- MONITOR LOOP ----------------
def monitor():
    while True:
        for chat_id, data in tracking.items():
            if not data["active"]:
                continue

            available = check_tickets(
                data["from"],
                data["to"],
                data["date"]
            )

            if available:
                bot.send_message(
                    chat_id,
                    f"🚆 Є квитки!\n\n{data['from']} → {data['to']}\n📅 {data['date']}\n\nЗаходь швидко в додаток!"
                )

                data["active"] = False

        time.sleep(60)  # перевірка кожну хвилину


# ---------------- RUN THREAD ----------------
threading.Thread(target=monitor, daemon=True).start()

print("Bot started...")
bot.infinity_polling()
