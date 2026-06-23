@bot.message_handler(
    func=lambda message: message.text in [
        "12.07", "13.07", "14.07", "15.07",
        "17:00", "20:25", "22:30"
    ]
)
def save_choice(message):
    if message.text in ["12.07", "13.07", "14.07", "15.07"]:
        if message.chat.id not in user_data:
            user_data[message.chat.id] = {}

        user_data[message.chat.id]["date"] = message.text

        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.row("17:00", "20:25")
        keyboard.row("22:30")
        keyboard.row("⬅️ Назад")

        bot.send_message(
            message.chat.id,
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
