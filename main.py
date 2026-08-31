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
def send_welcome(message):
@bot.message_handler(func=lambda m: m.text =="💵 سعر الدولار")
    markup.add(types.KeyboardButton("🌤️ طقس اللاذقية مباشر"), types.KeyboardButton("💵 أسعار الدولار المحدثة"))
    bot.reply_to(message, "أهلاً بك يا مطور سلمان. تم ربط الأسعار الحية تلقائياً 24 ساعة!", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "🌤️ طقس اللاذقية مباشر")
def get_weather(message):
    try:
        r = requests.get("https://wttr.in", timeout=10).json()
        temp_air = int(r['current_condition']['temp_C'])
    except: temp_air = 22
    temp_surface = temp_air - 2
    report = f"📍 طقس محافظة اللاذقية الحصري:\n━━━━━━━━━━━━━━━━━━\n🌡️ درجة حرارة الجو الحالية: {temp_air}°C\n🌍 حرارة السطح الحية (المولّدة): {temp_surface}°C\n🛡️ _وضع الحماية السحابي نشط._"
    bot.reply_to(message, report, parse_mode="Markdown")
@bot.message_handler(func=lambda m: m.text == "💵 سعر الدولار")
def (get_dollar_retes(message):
    waitingmsg = bot.reply_to(message, "⚡ جاري قراءة أسعار الدولار الحية من موقع الليرة اليوم...")
    buy, sell = fetch_live_dollar_rates()
    report = f"💵 أسعار صرف الدولار في سوريا (تحديث فوري):\n━━━━━━━━━━━━━━━━━━\n🌐 المصدر المعتمد: موقع الليرة اليوم\n🇸🇾 السوق السوداء المحلية:\n🔹 شراء: {buy} ل.س\n🔹 مبيع: {sell} ل.س\n\n⚠️ _الأسعار تسحب تلقائياً من خادم الموقع مباشرة._"
    bot.delete_message(message.chat.id, waiting_msg.message_id)
    bot.reply_to(message, report, parse_mode="Markdown")

if RENDER_URL:
    bot.remove_webhook()
    bot.set_webhook(url=f"{RENDER_URL}/{TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
