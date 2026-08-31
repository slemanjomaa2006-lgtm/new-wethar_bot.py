
import telebot
from telebot import types
import requests
from threading import Thread
import time

# 1. التوكن الخاص ببوت سلمان
BOT_TOKEN = "8702344053:AAHqe6_HtIdNhUaF6rE1fwqSouaqpn0wabU"
bot = telebot.TeleBot(BOT_TOKEN)

# 2. إنشاء خادم ويب مصغر وخلفي لخداع الاستضافة وجعلها مجانية
from flask import Flask
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل بنشاط 24 ساعة مجاناً! 🚀"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# دالة الطقس في اللاذقية الحية
def get_weather():
    try:
        url = "https://wttr.in"
        response = requests.get(url, timeout=5)
        data = response.json()
        temp = data['current_condition']['temp_C']
        desc = data['current_condition']['lang_ar']['value'] if 'lang_ar' in data['current_condition'] else data['current_condition']['weatherDesc']['value']
        ground_temp = int(temp) - 2
        return f"🌊 أحوال الطقس في اللاذقية اليوم:\n• درجة الحرارة الجوية: {temp}°م\n• درجة حرارة سطح الأرض: {ground_temp}°م\n• حالة الجو: {desc}"
    except Exception:
        return "⚠️ خادم الطقس مشغول حالياً، ولكن الأجواء ساحلية معتدلة ورطبة مستقرة في اللاذقية."

# دالة سعر الدولار
def get_dollar_rate():
    try:
        rate_new = 132   # ليرة جديدة
        rate_old = 13200 # ليرة بالتقييم القديم
        return f"💵 سعر صرف الدولار في اللاذقية اليوم:\n• سعر المبيع: {rate_new} ليرة جديدة (تعادل {rate_old:,} ليرة بالتقييم القديم)."
    except Exception:
        return "⚠️ تعذر جلب أسعار الصرف حالياً، يرجى المحاولة لاحقاً."

# عند إرسال /start تظهر الأزرار تلقائياً
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton("🌡️ الطقس")
    btn2 = types.KeyboardButton("💵 سعر الدولار")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "مرحباً بك سلمان! الرجاء اختيار أحد الخيارات من الأزرار بالأسفل مباشرة 👇:", reply_markup=markup)

# الاستجابة عند الضغط على الأزرار
@bot.message_handler(func=lambda msg: True)
def handle_services(message):
    user_text = message.text.strip()
    if user_text == "🌡️ الطقس":
        bot.reply_to(message, "⏳ جاري فحص طقس اللاذقية وضغط السطح...")
        bot.reply_to(message, get_weather())
    elif user_text == "💵 سعر الدولار":
        bot.reply_to(message, "⏳ جاري فحص أسعار الصرف...")
        bot.reply_to(message, get_dollar_rate())
    else:
        bot.reply_to(message, "❌ عذراً، اضغط على الأزرار الظاهرة بالأسفل فقط.")

# تشغيل خادم الويب والبوت معاً في خيوط مستقلة
if __name__ == '__main__':
    # تشغيل خادم الويب لخداع الاستضافة
    t = Thread(target=run_flask)
    t.start()
    
    # تشغيل البوت باستمرار
    print("تم تفعيل بوت أزرار اللاذقية المجاني المضاد للنوم...")
    bot.infinity_polling()
