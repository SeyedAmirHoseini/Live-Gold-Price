from telegram.ext import Updater, CommandHandler, JobQueue
from bot.config import *
from bot.handlers.commands import start, gold
import logging, requests
from datetime import datetime
from telegram import Bot
import time, threading


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# متغیر سراسری برای نگهداری قیمت از آخرین پیام ارسال شده
last_sent_message_price = None

price_updated_event = threading.Event()

# محدوده زمانی مارکت طلا
now = datetime.now()
OPEN_MARKET = datetime(now.year, now.month, now.day, 10, 0)
CLOSE_MARKET = datetime(now.year, now.month, now.day, 21, 0)


bot = Bot(token=BOT_TOKEN)

def get_current_price(response):
    if response.status_code == 200:
        data = response.json()
        golds = data['gold']
        for gold in golds:
            if gold['name'] == "طلای 18 عیار":
                price = gold['price']
                print(f" Current price found: {price}$")
                return price      
    return None


def send_price(context):
    global last_sent_message_price

    response = requests.get(API_URL)

    current_time = datetime.now().time()
    price = get_current_price(response)
    print(f"Last sent message is: {price}")
    context.bot.send_message(chat_id=CHAT_ID, text=f"قیمت فعلی طلای 18 عیار: {price}")
    print("Message has been sent!")
    last_sent_message_price = price


def get_last_message():
    messages = bot.get_chat_history(chat_id=CHAT_ID, limit=1)
    if messages:
        message = messages[0]
        parts = message.split(":")
        price = int(parts[-1].strip())
        return price
    return None


def price_jump():
    global last_sent_message_price
    if last_sent_message_price == None:
        response = requests.get(API_URL)
        last_sent_message_price = get_current_price(response)

    while True:   
        print(f"Threading Loading... (Price: {last_sent_message_price})")

        response = requests.get(API_URL)
        current_price = get_current_price(response)
        print("Looking for a big CHANGE...")
        if (last_sent_message_price is not None) and (abs(current_price - last_sent_message_price) > 1000):
            print(f"Finally a BIG change! Price is now: {current_price}")
            message = f"فوری*\nقیمت طلا 18 عیار : {current_price}"
            bot.send_message(chat_id=CHAT_ID, text=message)
            last_sent_message_price = current_price

        time.sleep(45)

        

def schedule_messages(job_queue):
    job_queue.run_repeating(send_price, interval=180, first=0)


def stop_sending_messages(job_queue):
    job_queue.stop()


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("gold", gold))

    job_queue = updater.job_queue

    schedule_messages(job_queue)

    job_queue.run_daily(stop_sending_messages, time=OPEN_MARKET)
    job_queue.run_daily(schedule_messages, time=CLOSE_MARKET)

    threading.Thread(target=price_jump, daemon=True).start()

    try:
        updater.start_polling()
    except KeyboardInterrupt:
        print("Bot stopped by user")
        updater.stop()
    finally:
        updater.idle()


if __name__ == '__main__':
    main()