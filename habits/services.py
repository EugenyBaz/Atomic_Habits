import requests
from config import settings

def send_telegram_message(chat_id, message):
    try:
        params = {
            'text':message,
            'chat_id':chat_id,
        }
        response = requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_BOT_TOKEN}/sendMessage', params=params)
        response.raise_for_status()  # Проверка статуса ответа


    except requests.HTTPError as error:
        if hasattr(error, 'text') and hasattr(error.response, 'text'):
            print(f'Ошибка отправки сообщения: {error.response.text}')
