import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from lorabot import LoraBot

lora_bot = LoraBot()
vk_session = vk_api.VkApi(token="")
bot = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def answer_text(vk_id, text):
    bot.messages.send(user_id=vk_id, message=text, random_id=0)


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            message = event.answer_text.lower()
            user_id = event.user_id
            lora_bot.user(user_id, "MyAnalyticBot")
            if message.startswith("analytics"):
                # enter keyword and password, divide them by space
                text = message.split(' ')
                if lora_bot.check_password(text[1]):
                    if text[2] == 'sql':
                        info = lora_bot.sql(message)
                        answer_text(user_id, info)
                    else:
                        photo, info = lora_bot.analyze_new_user('MyAnalyticBot')
                        answer_text(user_id, info)
                        photo, info = lora_bot.analyze_dau('MyAnalyticBot')
                        answer_text(user_id, info)

            elif message == "Hi":
                lora_bot.message(message, 'text', user_id, "MyAnalyticBot")
                answer_text(user_id, 'Hi!')
            else:
                lora_bot.message(message, 'text', user_id, "MyAnalyticBot")
                answer_text(user_id, 'What?')
