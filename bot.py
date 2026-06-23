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
