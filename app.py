import os
import requests
from flask import Flask, request

app = Flask(__name__)

# دریافت توکن و کلید از متغیرهای محیطی
TELEGRAM_TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# آدرس وب‌هوک تلگرام
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    user_message = data['message']['text']
    
    # ارسال درخواست به OpenAI برای اصلاح گرامر
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": f"Correct the grammar: {user_message}"}],
            "max_tokens": 100
        }
    )
    
    corrected_message = response.json()['choices'][0]['message']['content']
    
    # ارسال پیام اصلاح‌شده به کاربر در تلگرام
    requests.post(BASE_URL, json={
        "chat_id": chat_id,
        "text": corrected_message
    })
    
    return 'OK'

if __name__ == '__main__':
    app.run(port=5000)
