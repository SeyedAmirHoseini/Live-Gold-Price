# 💰 Live Gold Prices Telegram Bot

A Telegram bot that fetches **live 18K gold prices** from [BrsApi.ir](https://BrsApi.ir) and sends:
- 🔔 **Urgent alerts** if there's a major price change (every 45 seconds check)
- 🕒 **Regular updates** every 3 minutes if there's no significant change

---

## 📡 API Source

The bot uses the following API for real-time data:
```
https://BrsApi.ir/Api/Market/Gold_Currency.php
```

---

## 🤖 Telegram Bot

You can use the bot here:  
👉 [@live_prices_bot](https://t.me/live_prices_bot)

Or follow the live updates in the channel:  
📢 [@live_gold_prices](https://t.me/live_gold_prices)

---

## ⚙️ How It Works

1. Every **45 seconds**, the bot checks for price updates.
2. If the **18K gold price** has changed significantly (based on a threshold you define), it sends an **urgent alert**.
3. If there’s no major change, it sends a **regular update** every 3 minutes.

---

## 🧠 Features

- Uses [`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot) for smooth Telegram interaction.
- Clean message formatting for clarity.
- Channel and private bot support.

---

## 📦 Installation

```bash
git clone https://github.com/SeyedAmirHoseini/Live-Gold-Price.git
virtual-env/scripts/activate
cd virtual-env
pip install -r requirements.txt