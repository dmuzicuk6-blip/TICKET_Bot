@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row("📅 Обрати дату")
    keyboard.row("⏰ Обрати час")
    keyboard.row("✍️ Ввести вручну")

    bot.send_message(
        message.chat.id,
        "Привіт! Обери дію:",
        reply_markup=keyboard
    )
@bot.message_handler(func=lambda message: message.text == "📅 Обрати дату")
def choose_date(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row("12.07", "13.07")
    keyboard.row("14.07", "15.07")
    keyboard.row("⬅️ Назад")

    bot.send_message(
        message.chat.id,
        "Обери дату:",
        reply_markup=keyboard
    )
    @bot.message_handler(func=lambda message: message.text in ["12.07", "13.07", "14.07", "15.07"])
def date_selected(message):
    bot.send_message(
        message.chat.id,
        f"Дата збережена: {message.text}"
    )
