import os
import requests
import openai
from flask import Flask, request

app = Flask(__name__)

# دریافت توکن و کلید از متغیرهای محیطی
TELEGRAM_TOKEN = os.getenv("TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# پیکربندی کتابخانه openai
openai.api_key = OPENAI_API_KEY

# آدرس وب‌هوک تلگرام
BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    user_message = data['message']['text']
    
    # ارسال درخواست به OpenAI برای اصلاح گرامر
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Correct the grammar: {user_message}"}],
        max_tokens=100
    )
    
    corrected_message = response['choices'][0]['message']['content']
    
    # ارسال پیام اصلاح‌شده به کاربر در تلگرام
    requests.post(BASE_URL, json={
        "chat_id": chat_id,
        "text": corrected_message
    })
    
    return 'OK'

if __name__ == '__main__':
    app.run()

