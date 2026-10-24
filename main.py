import os
import telebot
from flask import Flask, request
import yt_dlp

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
      "Salom! Menga Instagram havolasini yuboring, men sizga videoni"
      " topib beraman.",
  )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
  text = message.text
  if "instagram.com" in text:
    msg = bot.reply_to(
        message, "⏳ Havola qabul qilindi! Video yuklab olinmoqda..."
    )

    try:
      ydl_opts = {
          'format': 'best',
          'outtmpl': 'video.mp4',
          'max_filesize': 50 * 1024 * 1024,
      }

      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([text])

      if os.path.exists('video.mp4'):
        with open('video.mp4', 'rb') as vid:
          bot.send_video(message.chat.id, vid, caption="Mana siz so'ragan video! 🎵")
        os.remove('video.mp4')
        bot.delete_message(message.chat.id, msg.message_id)
      else:
        bot.edit_message_text(
            "Kechirasiz, videoni yuklab bo'lmadi.",
            message.chat.id,
            msg.message_id,
        )

    except Exception as e:
      bot.edit_message_text(
          f"Xatolik yuz berdi: {str(e)}", message.chat.id, msg.message_id
      )
  else:
    bot.reply_to(message, "Iltimos, to'g'ri Instagram havolasini yuboring.")


if __name__ == "__main__":
  RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
  if RENDER_URL:
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")

  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)

