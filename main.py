import telebot

TOKEN = "8933061889:AAHnMZGVi0s02wdpmdTSJ_xPHYZIFligvFs"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Menga musiqa nomini yuboring.")

bot.infinity_polling()
