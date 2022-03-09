import telebot
from telebot import types
from lorabot import LoraBot

token = ""
bot = telebot.TeleBot(token)
lora_bot = LoraBot('MyAnalyticBot')

user_markup = types.ReplyKeyboardMarkup(True)
menu = ['Menu a', 'Menu b', 'Make order', 'Leave review', 'Leave rating']
user_markup.row(menu[0], menu[1])
user_markup.row(menu[2])
user_markup.row(menu[3], menu[4])

buy_markup = types.ReplyKeyboardMarkup(True)
menu_buy = ['Return', 'Buy']
buy_markup.row(menu_buy[1])
buy_markup.row(menu_buy[0])

analytics_markup = types.ReplyKeyboardMarkup(True)
menu_analytics = ['Total', 'Users', 'Messages', 'Events', 'Rating', 'SQL']
analytics_markup.row(menu_analytics[0], menu_analytics[1])
analytics_markup.row(menu_analytics[2], menu_analytics[3])
analytics_markup.row(menu_analytics[4])
analytics_markup.row(menu_analytics[5])

no_markup = types.ReplyKeyboardMarkup(True)
no_markup.row('No')

user_analytics = {}


def message_password(message):
    if lora_bot.check_password(message.text):
        bot.send_message(message.chat.id, "Choose what you want to analyze", reply_markup=analytics_markup)
        bot.register_next_step_handler(message, analytics)
    else:
        bot.send_message(message.chat.id, "Error", reply_markup=user_markup)


def analytics(message):
    if message.text == 'SQL':
        bot.send_message(message.chat.id, "Write your SQL", reply_markup=no_markup)
        user_analytics[message.from_user.id] = {}
        user_analytics[message.from_user.id]['analytics_type'] = message.text
        bot.register_next_step_handler(message, analytics_date)
    elif message.text in menu_analytics:
        bot.send_message(message.chat.id, "Set date if you need(start and end date "
                                          "splitting by space in format 'YYYY-MM-DD')"
                                          " or select no on menu", reply_markup=no_markup)
        user_analytics[message.from_user.id] = {}
        user_analytics[message.from_user.id]['analytics_type'] = message.text
        bot.register_next_step_handler(message, analytics_date)
    else:
        bot.send_message(message.chat.id, "Error", reply_markup=user_markup)


def analytics_date(message):
    if user_analytics[message.from_user.id]['analytics_type'] == 'SQL':
        info = lora_bot.sql_query(message.text)
        bot.send_message(message.chat.id, info, reply_markup=user_markup)
        user_analytics[message.from_user.id] = {}
        bot.send_message(message.chat.id, "End analytics", reply_markup=user_markup)
    elif message.text == 'No':
        user_analytics[message.from_user.id]['start_date'] = None
        user_analytics[message.from_user.id]['end_date'] = None
        bot.send_message(message.chat.id, "Set message or event type (only this one has types) or select no on menu", reply_markup=no_markup)
        bot.register_next_step_handler(message, analytics_type)
    elif len(message.text.split(' ')) == 2:
        date = message.text.split(' ')
        user_analytics[message.from_user.id]['start_date'] = date[0]
        user_analytics[message.from_user.id]['end_date'] = date[1]
        bot.send_message(message.chat.id, "Set message or event type (only this one has types) or select no on menu", reply_markup=no_markup)
        bot.register_next_step_handler(message, analytics_type)
    else:
        bot.send_message(message.chat.id, "Error", reply_markup=user_markup)


def analytics_type(message):
    if message.text == 'No':
        user_analytics[message.from_user.id]['type'] = None
    else:
        user_analytics[message.from_user.id]['type'] = message.text
    if user_analytics[message.from_user.id]['analytics_type'] == 'Total':
        info = lora_bot.analyze_total(user_analytics[message.from_user.id]['start_date'],
                                                user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
    elif user_analytics[message.from_user.id]['analytics_type'] == 'Users':
        photo, info = lora_bot.analyze_new_user(user_analytics[message.from_user.id]['start_date'],
                                                user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        photo, info = lora_bot.analyze_user_number_accumulation(user_analytics[message.from_user.id]['start_date'],
                                                                user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        photo = lora_bot.analyze_hour_activity(user_analytics[message.from_user.id]['start_date'],
                                                     user_analytics[message.from_user.id]['end_date'])
        bot.send_photo(message.chat.id, photo)
        photo, info = lora_bot.analyze_dau(user_analytics[message.from_user.id]['start_date'],
                                           user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        photo, info = lora_bot.analyze_wau(user_analytics[message.from_user.id]['start_date'],
                                           user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        photo, info = lora_bot.analyze_mau(user_analytics[message.from_user.id]['start_date'],
                                           user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        photo, info = lora_bot.analyze_yau(user_analytics[message.from_user.id]['start_date'],
                                           user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        photo, info = lora_bot.analyze_language(user_analytics[message.from_user.id]['start_date'],
                                                user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
    elif user_analytics[message.from_user.id]['analytics_type'] == 'Messages':
        photo, info = lora_bot.analyze_messages_number(user_analytics[message.from_user.id]['start_date'],
                                                       user_analytics[message.from_user.id]['end_date'],
                                                       user_analytics[message.from_user.id]['type'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        info = lora_bot.analyze_messages(user_analytics[message.from_user.id]['start_date'],
                                                user_analytics[message.from_user.id]['end_date'],
                                                user_analytics[message.from_user.id]['type'])
        bot.send_message(message.chat.id, info)
        photo, info = lora_bot.analyze_messages_type(user_analytics[message.from_user.id]['start_date'],
                                                     user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        photo, info = lora_bot.analyze_messages_funnel(['Menu c', 'Menu b', 'Menu a'],
                                                       user_analytics[message.from_user.id]['start_date'],
                                                       user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
    elif user_analytics[message.from_user.id]['analytics_type'] == 'Events':
        photo, info = lora_bot.analyze_events_number(user_analytics[message.from_user.id]['start_date'],
                                                     user_analytics[message.from_user.id]['end_date'],
                                                     user_analytics[message.from_user.id]['type'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        info = lora_bot.analyze_events(user_analytics[message.from_user.id]['start_date'],
                                              user_analytics[message.from_user.id]['end_date'],
                                              user_analytics[message.from_user.id]['type'])
        bot.send_message(message.chat.id, info)
        photo, info = lora_bot.analyze_events_type(user_analytics[message.from_user.id]['start_date'],
                                                   user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        photo, info = lora_bot.analyze_events_funnel(['Menu received', 'Make order', 'Buy'],
                                                     user_analytics[message.from_user.id]['start_date'],
                                                     user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
    elif user_analytics[message.from_user.id]['analytics_type'] == 'Rating':
        photo, info = lora_bot.analyze_assessment(user_analytics[message.from_user.id]['start_date'],
                                                   user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
        bot.send_photo(message.chat.id, photo)
        info = lora_bot.analyze_review(user_analytics[message.from_user.id]['start_date'],
                                              user_analytics[message.from_user.id]['end_date'])
        bot.send_message(message.chat.id, info)
    user_analytics[message.from_user.id] = {}
    bot.send_message(message.chat.id, "End analytics", reply_markup=user_markup)


def rating(message):
    if message.text in ('1', '2', '3', '4', '5'):
        rating = int(message.text)
        lora_bot.assessment(rating, message.from_user.id)
        bot.send_message(message.chat.id, "Thank you!", reply_markup=user_markup)
    else:
        bot.send_message(message.chat.id, "Error", reply_markup=user_markup)


def review(message):
    lora_bot.review(message.text, message.from_user.id)
    bot.send_message(message.chat.id, "Thank you!", reply_markup=user_markup)


@bot.message_handler(commands=['start'])
def handle_text(message):
    lora_bot.user(message.from_user.id, message.from_user.language_code)
    lora_bot.event('Menu received', 'Order', message.from_user.id)
    bot.send_message(message.chat.id, "Hi! Choose commands or write message", reply_markup=user_markup)


@bot.message_handler(commands=['command_a', 'command_b'])
def handle_text(message):
    lora_bot.message(message.text, 'command', message.from_user.id)
    if message.text == 'command_b':
        lora_bot.event('Event for command that do something', 'Event simple command', message.from_user.id)
    bot.send_message(message.chat.id, f'You use the command {message.text}')


@bot.message_handler(commands=['secret'])
def handle_text(message):
    lora_bot.message(message.text, 'command', message.from_user.id)
    lora_bot.event('Event for secret command', 'Secret', message.from_user.id)
    bot.send_message(message.chat.id, f'You use the command {message.text}')


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "analytics":
        # make message chains for analytics
        bot.send_message(message.from_user.id, 'Enter password')
        bot.register_next_step_handler(message, message_password)
    else:
        if message.text == 'Make order':
            text = f'Press Buy or Return'
            lora_bot.message(message.text, 'menu', message.from_user.id)
            lora_bot.event('Make order', 'Order',  message.from_user.id)
            bot.send_message(message.chat.id, text, reply_markup=buy_markup)
        elif message.text == 'Buy':
            text = f'You use the menu command {message.text}'
            lora_bot.message(message.text, 'menu', message.from_user.id)
            lora_bot.event('Buy', 'Order',  message.from_user.id)
            bot.send_message(message.chat.id, text, reply_markup=user_markup)
        elif message.text == 'Leave rating':
            bot.send_message(message.from_user.id, 'Write the mark to bot(1-5):')
            bot.register_next_step_handler(message, rating)
        elif message.text == 'Leave review':
            bot.send_message(message.from_user.id, 'Write your review')
            bot.register_next_step_handler(message, review)
        elif message.text in menu:
            text = f'You use the menu command {message.text}'
            lora_bot.message(message.text, 'menu', message.from_user.id)
            bot.send_message(message.chat.id, text, reply_markup=user_markup)
        else:
            text = f'You write {message.text}'
            lora_bot.message(message.text, 'text', message.from_user.id)
            bot.send_message(message.chat.id, text, reply_markup=user_markup)


bot.polling(none_stop=True)