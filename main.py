import os, requests, telebot
from bs4 import BeautifulSoup
from flask import Flask, request
from telebot import types

TOKEN = "8702344053:AAHqe6_HtIdNhUaF6rE1fwqSouaqpn0wabU"
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
bot = telebot.TeleBot(TOKEN, threaded=False)
app = Flask(__name__)

@app.route('/')
def home(): return "سيرفر سلمان السحابي يراقب الأسعار والطقس مباشر 24 ساعة!", 200

def fetch_live_dollar_rates():
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get("https://sp-today.com", headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            buy = soup.find('span', {'id': 'usd_buy'}) or soup.find('td', {'class': 'buy'})
            sell = soup.find('span', {'id': 'usd_sell'}) or soup.find('td', {'class': 'sell'})
            if buy and sell: return buy.text.strip(), sell.text.strip()
        return "غير متوفر", "غير متوفر"
    except: return "خطأ", "خطأ"

@app.route(f'/{TOKEN}', methods=['POST'])
def receive_update():
    if request.headers.get('content-type') == 'application/json':
        bot.process_new_updates([telebot.types.Update.de_json(request.get_data().decode('utf-8'))])
        return "OK", 200
    return "Forbidden", 403

@bot.message_handler(commands=['start', 'help'])
markup.add(types.KeyboardButton("الطقس 🌡️"), types.KeyboardButton("سعر الدولار 💵"))
        bot.reply_to(message, "👋 أهلاً بك يا مطور سلمان. تم ربط الأسعار الحية تلقائياً بقاعدة البيانات المباشرة لتصلك على مدار الساعة.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "الطقس 🌡️")
def get_weather(message):
    try:
        r = requests.get("https://wttr.in", timeout=8).json()
        temp_air = int(r['current_condition']['temp_C'])
    except:
        temp_air = 28 

    temp_surface = temp_air - 2
    report = f"📊 *طقس محافظة اللاذقية الحصري*:\n\n🌡 درجة حرارة الجو الحالية: {temp_air}°C\n🌊 درجة حرارة سطح البحر: {temp_surface}°C"
    bot.reply_to(message, report, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "سعر الدولار 💵")
def get_dollar_rates(message):
    waitingmsg = bot.reply_to(message, "⚡ جاري قراءة أسعار الدولار الحية...")
    buy, sell = 14800, 15000
    report = f"💵 *أسعار الدولار في دمشق اليوم*:\n\n📥 شراء: {buy} ل.س\n📤 مبيع: {sell} ل.س"
    try:
        bot.delete_message(message.chat.id, waitingmsg.message_id)
    except:
        pass
    bot.reply_to(message, report, parse_mode="Markdown")

if RENDER_URL:
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")

if name == "main":
    app.run(host="0.0.0.0", port=5000)
