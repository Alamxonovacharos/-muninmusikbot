

import os
import telebot
from flask import Flask, request

TOKEN = '8933061889:AAHnMZGVi0s02wdpmdTSJ_xPHYZIFligvFs'
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
  json_string = request.get_data().decode("utf-8")
  update = telebot.types.Update.de_json(json_string)
  bot.process_new_updates([update])
  return "!", 200


@app.route("/")
def index():
  return "Bot is alive!", 200


@bot.message_handler(commands=['start'])
def send_welcome(message):
  bot.reply_to(
      message,
      "Salom! Menga Instagram yoki boshqa saytlardan havola yuboring.",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  text = message.text
  if "instagram.com" in text:
    bot.reply_to(
        message,
        "Havola qabul qilindi! Musiqani yuklab olish jarayoni boshlandi...",
    )
    # Bu yerga musiqa yuklab beruvchi kodni qo'shamiz
  else:
    bot.reply_to(message, "Iltimos, to'g'ri Instagram havolasini yuboring.")


if __name__ == "__main__":
  RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
  if RENDER_URL:
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")

  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)
