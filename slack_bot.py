import time
from slackclient import SlackClient
from lorabot import LoraBot


BOT_TOKEN = ""
lora_bot = LoraBot('MyAnalyticBot')


def main():
    slack_bot = SlackClient(BOT_TOKEN)

    if not slack_bot.rtm_connect():
        raise Exception("Couldn't connect to slack.")

    while True:
        for slack_event in slack_bot.rtm_read():
            if not slack_event.get('type') == "message":
                continue
            message = slack_event.get("text")
            user = slack_event.get("user")
            channel = slack_event.get("channel")
            if not message or not user:
                continue
            lora_bot.user(user, "MyAnalyticBot")
            if message.startswith("analytics"):
                # enter keyword and password, divide them by space
                text = message.split(' ')
                if lora_bot.check_password(text[1]):
                    photo, info = lora_bot.analyze_new_user('MyAnalyticBot')
                    slack_bot.rtm_send_message(channel, info)
            if message.find("help"):
                lora_bot.message(message, 'Help_Command', user, "MyAnalyticBot")
                slack_bot.rtm_send_message(channel, 'Hi!')
            else:
                lora_bot.message(message, 'text', user, "MyAnalyticBot")
                slack_bot.rtm_send_message(channel, '?!')

        time.sleep(0.5)


if __name__ == '__main__':
    main()