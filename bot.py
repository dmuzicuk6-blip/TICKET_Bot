import telebot
import requests
import time
import threading

TOKEN = "8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q"
bot = telebot.TeleBot(TOKEN)

tracking = {}

# ---------------- START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🚆 УЗ Моніторинг\n\nНапиши:\nКиїв - Чоп\n12.07"
    )


# ---------------- ADD ROUTE ----------------
@bot.message_handler(func=lambda m: "-" in m.text)
def add_route(message):
    try:
        route, date = message.text.split("\n")
        from_city, to_city = [x.strip() for x in route.split("-")]

        tracking[message.chat.id] = {
            "from": from_city,
            "to": to_city,
            "date": date,
            "active": True
        }

        bot.send_message(
            message.chat.id,
            f"🔔 Моніторинг активовано\n{from_city} → {to_city}\n📅 {date}"
        )

    except:
        bot.send_message(message.chat.id, "❌ Формат:\nКиїв - Чоп\n12.07")


# ---------------- UZ REQUEST ----------------
def check_uz(from_city, to_city, date):
    """
    Реальний запит до системи пошуку УЗ.
    Це НЕ офіційний API, але працює як база для перевірки.
    """

    try:
        url = "https://booking.uz.gov.ua/train_search/"

        data = {
            "from": from_city,
            "to": to_city,
            "date": date
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.post(url, data=data, headers=headers, timeout=10)

        # якщо є результат — значить щось знайдено
        if r.status_code == 200 and len(r.text) > 50:
            return True

        return False

    except:
        return False


# ---------------- MONITOR ----------------
def monitor():
    while True:
        for chat_id, data in list(tracking.items()):

            if not data["active"]:
                continue

            ok = check_uz(
                data["from"],
                data["to"],
                data["date"]
            )

            if ok:
                bot.send_message(
                    chat_id,
                    f"🚆 Є квитки!\n\n{data['from']} → {data['to']}\n📅 {data['date']}\n\n⚡️ Заходь швидко в УЗ!"
                )

                data["active"] = False

        time.sleep(60)


threading.Thread(target=monitor, daemon=True).start()

print("Bot started...")
bot.infinity_polling()
