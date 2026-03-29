import os
import telebot
from flask import Flask, request
from telebot.types import ReplyKeyboardMarkup

TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN not found in ENV")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# ===== TEXT =====

disclaimer = """⚠️ Disclaimer

This bot is created for educational purposes only.
Trading involves financial risk and may result in loss.
We do not provide financial advice, signals, or guaranteed results.

By continuing, you confirm that you understand and accept this.
"""

welcome = """This is not a signal service.

It’s a learning environment built to help you understand markets step by step.

Instead of guessing, you’ll learn how to:
• Observe market structure
• Think in probabilities
• Manage risk responsibly

Everything here is simplified for better understanding.

Start exploring below.
"""

market_structure = """📈 Market Structure

Markets move in phases:

• Uptrend → higher highs & higher lows
• Downtrend → lower highs & lower lows
• Range → sideways movement

Recognizing structure helps avoid random decisions.
"""

risk_awareness = """⚖️ Risk Awareness

Risk matters more than results.

Basic principles:
• Never risk more than you can handle
• Protect capital first
• Avoid emotional decisions

Good risk control keeps you in the game.
"""

chart_reading = """🔍 Chart Reading

Charts tell a story.

Focus on:
• Key levels (support/resistance)
• Reaction points
• Price behavior, not predictions

Clarity comes from observation, not guessing.
"""

support = """📩 Support

For questions about learning topics or guidance:

Contact: @tradewithparul

Support is limited to educational discussions only.
No trading advice or signals are provided.
"""


# ===== MENU =====

def menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("📈 Market Structure", "⚖️ Risk Awareness")
    kb.row("🔍 Chart Reading", "📩 Support")
    return kb


# ===== START =====

@bot.message_handler(commands=['start'])
def start(msg):

    d = bot.send_message(msg.chat.id, disclaimer)

    try:
        bot.pin_chat_message(msg.chat.id, d.message_id)
    except:
        pass

    bot.send_message(msg.chat.id, welcome, reply_markup=menu())


# ===== BUTTONS =====

@bot.message_handler(func=lambda m: m.text == "📈 Market Structure")
def b1(m):
    bot.send_message(m.chat.id, market_structure)

@bot.message_handler(func=lambda m: m.text == "⚖️ Risk Awareness")
def b2(m):
    bot.send_message(m.chat.id, risk_awareness)

@bot.message_handler(func=lambda m: m.text == "🔍 Chart Reading")
def b3(m):
    bot.send_message(m.chat.id, chart_reading)

@bot.message_handler(func=lambda m: m.text == "📩 Support")
def b4(m):
    bot.send_message(m.chat.id, support)


# ===== WEBHOOK =====

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.stream.read().decode("utf-8"))]
    )
    return "ok", 200


@app.route("/")
def home():
    return "Bot Running"


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(
        url=os.environ.get("RENDER_EXTERNAL_URL") + "/" + TOKEN
    )
    app.run(host="0.0.0.0", port=10000)
