@bot.message_handler(func=lambda message: message.text in [
    "12.07", "13.07", "14.07", "15.07",
    "17:00", "20:25", "22:30"
])
def save_choice(message):
    chat_id = message.chat.id

    if chat_id not in user_data:
        user_data[chat_id] = {}

    # якщо це дата
    if message.text in ["12.07", "13.07", "14.07", "15.07"]:
        user_data[chat_id]["date"] = message.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row("17:00", "20:25")
        keyboard.row("22:30")
        keyboard.row("⬅️ Назад")

        bot.send_message(
            chat_id,
            "Ок, дату збережено. Обери час:",
            reply_markup=keyboard
        )

    # якщо це час
    else:
        user_data[chat_id]["time"] = message.text

        bot.send_message(
            chat_id,
            f"Готово ✅\nДата: {user_data[chat_id].get('date')}\nЧас: {message.text}"
        )
            f"Дата збережена: {message.text}\nТепер обери час:",
            reply_markup=keyboard
        )

    else:
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {}

        user_data[message.chat.id]["time"] = message.text

        date = user_data[message.chat.id].get("date", "не вибрана")

        bot.send_message(
            message.chat.id,
            f"✅ Готово!\nДата: {date}\nЧас: {message.text}"
        )
