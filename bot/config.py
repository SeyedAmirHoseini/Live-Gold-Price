import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

API_URL = f"https://BrsApi.ir/Api/Market/Gold_Currency.php?key={API_KEY}"

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHAT_ID = "@live_gold_prices"