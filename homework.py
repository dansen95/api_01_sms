import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

ACCOUNT_SID = os.getenv('SID')
SMS_TOKEN = os.getenv('AUTH_TOKEN')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')

client = Client(ACCOUNT_SID, SMS_TOKEN)

BASE_URL = 'https://api.vk.com/method/users.get'
VK_TOKEN = os.getenv('TOKEN')
API_V = '5.92'


def get_status(user_id):
    params = {
        'user_id': user_id,
        'v': API_V,
        'fields': 'online',
        'access_token': VK_TOKEN,
    }
    friends_list = requests.post(BASE_URL, params=params)
    return friends_list.json()['response'][0]['online']


def send_sms(sms_text):
    message = client.messages.create(
        to = NUMBER_TO,
        from_= NUMBER_FROM,
        body = sms_text
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
