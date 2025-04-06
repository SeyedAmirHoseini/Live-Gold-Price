from telegram import Update
from telegram.ext import CallbackContext
from bot.config import API_URL
import requests

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! برای دریافت قیمت طلا، دستور /gold را وارد کنید.")


def gold(update: Update, context: CallbackContext):
    response = requests.get(API_URL)

    if response.status_code == 200:
        data = response.json()
        golds = data['gold']
        for gold in golds:
            if gold['name'] == 'گرم طلای 18 عیار':
                price = gold['price']
                break
        try:
            update.message.reply_text(f"قیمت طلا: {price} تومان")
        except:
            update.message.reply_text(f"قیمت طلا یافت نشد")
    else:
        update.message.reply_text("خطا در دریافت قیمت طلا.")