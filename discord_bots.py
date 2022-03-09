import discord
from lorabot import LoraBot

client = discord.Client()
lora_bot = LoraBot()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    else:
        lora_bot.user(message.author, "MyAnalyticBot")

    if message.content.startswith("analytics"):
        # enter keyword and password, divide them by space
        text = message.content.split(' ')
        if lora_bot.check_password(text[1]):
                photo, info = lora_bot.analyze_new_user('MyAnalyticBot')
                await message.channel.send(info)
                await message.channel.send(file=discord.File(photo))
    elif message.content.startswith('Hi!'):
        lora_bot.message(message.content, 'text', message.author, "MyAnalyticBot")
        await message.channel.send('Hello!')
    else:
        lora_bot.message(message.content, 'text', message.author, "MyAnalyticBot")
        await message.channel.send('!?')

token = ''
client.run(token)