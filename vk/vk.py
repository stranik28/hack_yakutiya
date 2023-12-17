import requests
import vk_api


# Устанавливаем подключение к VK
token = 'vk1.a.0RLveaBz8bQXp4wR5oR89QGEteaTyJzihjKsNSdvahRaKXK-WCDljwSbQoWaBbILZZQvCwYGHV4joNPoHsu_r15FNl7kQjC4zclSdEtb6gV24Jgw5pflRgPq7Kd2mHOj-CYtVx-kfII2QFVrmO_MLSZdhuIjjtEdsJ-AsbaYnA7GU9-TBbIY3ZeP0jgcBs4Nv6GaoFlgPEJ5bJuHChYPzQ'
vk_session = vk_api.VkApi(token=token)
from vk_api.longpoll import VkLongPoll, VkEventType
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
        message = requests.get(f'http://fastapi:8000/process_message/?message={event.text}')
        message = message.json()['STATUS']
        if event.from_user: #Если написали в ЛС
            vk.messages.send( #Отправляем сообщение
                user_id=event.user_id,
                message=message,
                random_id=0
            )