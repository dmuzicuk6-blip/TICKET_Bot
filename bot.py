import telebot

TOKEN = "8422214558:AAFDJ8_6NzYIh3xKoplMLHd5gXijW1Rvk2Q"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "OK працює")

print("Bot started...")
bot.infinity_polling()
