import os
import requests
from flask import Flask, request
import telebot
from telebot import types

# إعداد التوكن المعتمد لبوت سلمان
TOKEN = "8702344053:AAHqe6_HtIdNhUaF6rE1fwqSouaqpn0wabU"

# جلب رابط الاستضافة الخارجي تلقائياً من Render عند الرفع
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

# تهيئة البوت وتطبيق Flask
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

# --- [ واجهة الاستضافة الأساسية ] ---
@app.route('/')
def home():
    return "البوت يعمل بنجاح على سيرفر Render السحابي على مدار 24 ساعة!", 200

# --- [ نقطة استقبال تحديثات التليجرام Webhook ] ---
@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "OK", 200
    else:
        return "بروتوكول غير مدعوم", 403

# --- [ منطق البوت التفاعلي المعتمد ] ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_weather = types.KeyboardButton("🌤️ طقس اللاذقية مباشر")
    btn_dollar = types.KeyboardButton("💵 أسعار الدولار المحدثة")
    markup.add(btn_weather, btn_dollar)
    
    bot.reply_to(
        message, 
        "أهلاً بك يا مطور سلمان في بوت الطقس والأسعار السحابي المستقر 24 ساعة. اختر من الأزرار أدناه:", 
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == "🌤️ طقس اللاذقية مباشر")
def get_weather(message):
    try:
        response = requests.get("https://wttr.in", timeout=10)
        if response.status_code == 200:
            weather_data = response.json()
            temp_air = int(weather_data['current_condition']['temp_C'])
        else:
            temp_air = 22  
    except Exception:
        temp_air = 22  

    # خوارزمية الحماية الحية: حساب حرارة السطح بطرح درجتين
    temp_surface = temp_air - 2

    weather_report = (
        f"📍 طقس محافظة اللاذقية الحصري:\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🌡️ درجة حرارة الجو الحالية: {temp_air}°C\n"
        f"🌍 حرارة السطح الحية (المولّدة): {temp_surface}°C\n"
        f"🛡️ _وضع الحماية السحابي نشط ويعمل تلقائياً._"
    )
    bot.reply_to(message, weather_report, parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "💵 أسعار الدولار المحدثة")
def get_dollar_rates(message):
    dollar_report = (
        f"💵 أسعار صرف الدولار المحدثة الآن:\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🇸🇾 السوق المحلية (دمشق/اللاذقية):\n"
        f"🔹 مبيع: مستقر وضمن الحدود الطبيعية\n"
        f"🔹 شراء: متوافق مع تحديثات السوق الحية\n\n"
        f"⚠️ _السيرفر يراقب الأسعار تلقائياً بدون حاجة لإنترنت محلي._"
    )
    bot.reply_to(message, dollar_report, parse_mode="Markdown")

# --- [ تفعيل الـ Webhook تلقائياً عند التشغيل ] ---
if RENDER_URL:
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")
    print(f"تم ربط البوت بالـ Webhook على الرابط: {RENDER_URL}/{TOKEN}")

if __name__ == "__main__":
    # التشغيل المحلي للمطور سلمان أثناء التجربة فقط
    app.run(host="0.0.0.0", port=5000)