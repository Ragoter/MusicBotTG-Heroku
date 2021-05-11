import vk_api
import requests
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json

session = requests.Session()
vk_session = vk_api.VkApi(token='b5ebe2ce0b75a30fc05ff36b4abfd648287eea53638220787c22597b79cd9c4d56390df223136636bb5e7')
try:
    vk_session.auth(token_only=True)
except vk_api.AuthError as error_msg:
    print(error_msg)
from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()

keyboard = {
    "one_time": False,
    "buttons": [
        [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Negative"
                },
                "color": "negative"
            }],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Positive"
                },
                "color": "positive"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Primary"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Secondary"
                },
                "color": "secondary"
            }
        ]
    ]
}
 
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))

def out_message(out_message): # 
    if event.from_user:
            vk.messages.send(
                user_id = event.user_id,
                message = out_message,
                random_id = random.getrandbits(64)
            )

for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
   #Слушаем longpoll, если пришло сообщение то:			
        if event.text == 'Привет' or event.text == 'привет': #Если написали заданную фразу
            out_message('И тебе')
            print('0')
        elif event.text == 'Хай' or event.text == 'хай':
                out_message('Хай')
                print('1')
        elif event.text == 'Negative':
            out_message('Красный')
        elif event.text == 'Positive':
            out_message('Зелёный')
        elif event.text == 'Primary':
            out_message('Белый')
        elif event.text == 'Secondary':
            out_message('Черный')       
        else:
            out_message('Не знаю что ответить')
            print('2')
        