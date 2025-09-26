import os
import requests

TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')

def send_telegram(message: str):
    if not TG_TOKEN or not TG_CHAT_ID:
        print("Telegram token or chat_id not set in .env")
        return
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {
        "chat_id": TG_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram alert sent")
        else:
            print("Failed to send Telegram alert:", response.text)
    except Exception as e:
        print("Error sending Telegram alert:", e)
