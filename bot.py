import telebot
from telebot import types
import sqlite3
import threading
import time
import requests

TOKEN = "8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q"
bot = telebot.TeleBot(TOKEN)

# ---------------- DATABASE ----------------
conn = sqlite3.connect("uz.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tracks (
    chat_id INTEGER,
    from_city TEXT,
    to_city TEXT,
    date TEXT,
    active INTEGER
)
""")
conn.commit()


# ---------------- /START ----------------
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("➕ Додати маршрут", "📡 Мої маршрути")

    bot.send_message(
        message.chat.id,
        "🚆 Бот моніторингу УЗ\n\nОбери дію:",
        reply_markup=keyboard
    )


# ---------------- MENU ----------------
@bot.message_handler(func=lambda m: m.text == "➕ Додати маршрут")
def add_route(message):
    msg = bot.send_message(
        message.chat.id,
        "Напиши так:\nКиїв - Чоп\n12.07"
    )
    bot.register_next_step_handler(msg, save_route)


def save_route(message):
    try:
        route, date = message.text.split("\n")
        from_city, to_city = [x.strip() for x in route.split("-")]

        cur.execute(
            "INSERT INTO tracks VALUES (?, ?, ?, ?, 1)",
            (message.chat.id, from_city, to_city, date)
        )
        conn.commit()

        bot.send_message(
            message.chat.id,
            f"🔔 Додано:\n{from_city} → {to_city}\n📅 {date}"
        )

    except:
        bot.send_message(message.chat.id, "❌ Невірний формат")


# ---------------- LIST ----------------
@bot.message_handler(func=lambda m: m.text == "📡 Мої маршрути")
def list_routes(message):
    cur.execute(
        "SELECT from_city, to_city, date FROM tracks WHERE chat_id=? AND active=1",
        (message.chat.id,)
    )
    rows = cur.fetchall()

    if not rows:
        bot.send_message(message.chat.id, "Нема активних маршрутів")
        return

    text = "📡 Активні маршрути:\n\n"
    for r in rows:
        text += f"🚆 {r[0]} → {r[1]} ({r[2]})\n"

    bot.send_message(message.chat.id, text)


# ---------------- UZ CHECK (СПРОЩЕНА, СТАБІЛЬНА) ----------------
def check_uz(from_city, to_city, date):
    try:
        url = "https://booking.uz.gov.ua/"
        r = requests.get(url, timeout=10)

        # якщо сайт відкривається — вважаємо що "є шанс квитків"
        if r.status_code == 200:
            return True

        return False

    except:
        return False


# ---------------- MONITOR ----------------
def monitor():
    while True:
        cur.execute("SELECT * FROM tracks WHERE active=1")
        rows = cur.fetchall()

        for chat_id, from_city, to_city, date, active in rows:

            if check_uz(from_city, to_city, date):
                bot.send_message(
                    chat_id,
                    f"🚆 МОЖЛИВО Є КВИТКИ!\n\n{from_city} → {to_city}\n📅 {date}\n\n⚡️ Перевір УЗ швидко!"
                )

                cur.execute("""
                    UPDATE tracks
                    SET active=0
                    WHERE chat_id=? AND from_city=? AND to_city=? AND date=?
                """, (chat_id, from_city, to_city, date))
                conn.commit()

        time.sleep(60)


# ---------------- START THREAD ----------------
threading.Thread(target=monitor, daemon=True).start()

print("Bot started...")
bot.infinity_polling()
