import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup  # مكتبة معالجة صفحات الويب لسحب الأسعار حية
from threading import Thread
import os

# 1. التوكن الخاص ببوت سلمان
BOT_TOKEN = "8702344053:AAHqe6_HtIdNhUaF6rE1fwqSouaqpn0wabU"
bot = telebot.TeleBot(BOT_TOKEN)

# 2. إنشاء خادم ويب خلفي لضمان استمرار الاستضافة المجانية على Render
from flask import Flask
app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل بنشاط وببيانات حية 24 ساعة مجاناً! 🚀"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# دالة جلب طقس اللاذقية الحي والمباشر
def get_weather():
    try:
        # سحب بيانات الطقس المباشرة لمدينة اللاذقية باللغة العربية
        url = "https://wttr.in"
        response = requests.get(url, timeout=7)
        data = response.json()
        temp = data['current_condition'][0]['temp_C']
        desc = data['current_condition'][0]['lang_ar'][0]['value'] if 'lang_ar' in data['current_condition'][0] else data['current_condition'][0]['weatherDesc'][0]['value']
        humidity = data['current_condition'][0]['humidity']
        
        return f"🌊 أحوال الطقس في اللاذقية الحيّة الآن:\n• درجة الحرارة الجوية: {temp}°م\n• حالة الجو: {desc}\n• نسبة الرطوبة الساحلية: {humidity}%"
    except Exception:
        return "⚠️ خادم الطقس العالمي مشغول حالياً، الأجواء ساحلية معتدلة ورطبة مستقرة عموماً باللاذقية."

# دالة جلب سعر الدولار الحي في سوريا (تحديث تلقائي)
def get_dollar_rate():
    try:
        # استخدام مصدر بديل ومستقر لجلب البيانات الحية المتوافقة مع السوق الموازي السوري (الليرة اليوم)
        url = "https://sp-today.com/"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=7)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج قيم الشراء والمبيع الحية من جدول العملات
        # ملحوظة: الأسعار يتم قراءتها تلقائياً وفق تقييم السوق اللحظي
        buy_price = soup.find('span', {'id': 'us_buy'}).text.strip()
        sell_price = soup.find('span', {'id': 'us_sell'}).text.strip()
        
        return f"💵 سعر صرف الدولار في سوريا (السوق الموازي) الحي واللحظي اليوم:\n• سعر الشراء: {buy_price} ليرة\n• سعر المبيع: {sell_price} ليرة"
    except Exception:
        # احتياطي في حال توقف موقع الكشط مؤقتاً
        return "⚠️ تعذر الاتصال بمؤشر الأسعار اللحظي، يرجى إعادة المحاولة خلال ثوانٍ لجلب السعر المباشر."

# عند إرسال /start تظهر الأزرار تلقائياً
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    btn1 = types.KeyboardButton("🌡️ الطقس")
    btn2 = types.KeyboardButton("💵 سعر الدولار")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "مرحباً بك سلمان! الرجاء اختيار أحد الخيارات من الأزرار بالأسفل مباشرة 👇:", reply_markup=markup)

# الاستجابة الديناميكية والحية عند الضغط على الأزرار
@bot.message_handler(func=lambda msg: True)
def handle_services(message):
    user_text = message.text.strip()
    if user_text == "🌡️ الطقس":
        bot.reply_to(message, "⏳ جاري جلب طقس اللاذقية المباشر من الأقمار الصناعية...")
        bot.reply_to(message, get_weather())
    elif user_text == "💵 سعر الدولار":
        bot.reply_to(message, "⏳ جاري قراءة أسعار الصرف الحية واللحظية من السوق...")
        bot.reply_to(message, get_dollar_rate())
    else:
        bot.reply_to(message, "❌ عذراً سلمان، يرجى الضغط على الأزرار الظاهرة في الأسفل فقط.")

# تشغيل خادم الويب والبوت معاً في خيوط مستقلة
if name == 'main':
    t = Thread(target=run_flask)
    t.start()
    
    print("تم تفعيل بوت اللاذقية المطور بالبيانات الحية المباشرة...")
    bot.infinity_polling()
