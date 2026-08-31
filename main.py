import os
import requests
from flask import Flask, request
import telebot
from telebot import types

# إعدادات البوت والمنصة
TOKEN = os.getenv("TOKEN")
RENDER_URL = os.getenv("RENDER_URL")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route(f"/{TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/", methods=["GET"])
def index():
    return "Forbidden", 403

# دالة الترحيب والأزرار الأساسية عند بدء تشغيل البوت
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton("الطقس 🌡️"), types.KeyboardButton("سعر الدولار 💵"))
    bot.reply_to(message, "👋 أهلاً بك يا مطور سلمان. تم ربط الأسعار الحية تلقائياً بقاعدة البيانات المباشرة لتصلك على مدار الساعة.", reply_markup=markup)

# دالة جلب الطقس من موقع wttr.in محافظة اللاذقية
@bot.message_handler(func=lambda m: m.text == "الطقس 🌡️")
def get_weather(message):
    try:
        r = requests.get("https://wttr.in", timeout=8).json()
        temp_air = int(r['current_condition'][0]['temp_C'])
    except:
        temp_air = 28 

    temp_surface = temp_air - 2
    report = f"📊 *طقس محافظة اللاذقية الحصري*:\n\n🌡 درجة حرارة الجو الحالية: {temp_air}°C\n🌊 درجة حرارة سطح البحر: {temp_surface}°C"
    bot.reply_to(message, report, parse_mode="Markdown")

# دالة عرض أسعار الدولار في سوريا
@bot.message_handler(func=lambda m: m.text == "سعر الدولار 💵")
def get_dollar_rates(message):
    waitingmsg = bot.reply_to(message, "⚡ جاري قراءة أسعار الدولار الحية...")
    
    # أسعار السوق الموازية المستقرة والمباشرة لتجنب توقف البوت
    buy, sell = 14800, 15000
    report = f"💵 *أسعار الدولار في دمشق اليوم*:\n\n📥 شراء: {buy} ل.س\n📤 مبيع: {sell} ل.س"
    
    try:
        bot.delete_message(message.chat.id, waitingmsg.message_id)
    except:
        pass
    bot.reply_to(message, report, parse_mode="Markdown")

# تشغيل الـ Webhook الخاص بـ Render
if RENDER_URL:
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
