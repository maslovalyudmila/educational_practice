# импортируем необходимые библиотеки
import telebot
from telebot import types
import sqlite3

# объявим переменную, в которой будем хранить токен нашего бота
token = 'my_bot'
bot = telebot.TeleBot(token)

# определим словарь для хранения значений, выбранных юзером
user_data = {
    'shelter_data': '',
    'pet_data': ''
}

# cоздадим словари с набором вариантов ответов
p_zoopomosch_cats = {'shelter_data': 'p_zoopomosch', 'pet_data': 'choose_cat'}
p_zoopomosch_dogs = {'shelter_data': 'p_zoopomosch', 'pet_data': 'choose_dog'}
p_kotedzh_cats = {'shelter_data': 'p_kotedzh', 'pet_data': 'choose_cat'}
p_kotedzh_dogs = {'shelter_data': 'p_kotedzh', 'pet_data': 'choose_dog'}
zrc_totoshka_cats = {'shelter_data': 'zrc_totoshka', 'pet_data': 'choose_cat'}
zrc_totoshka_dogs = {'shelter_data': 'zrc_totoshka', 'pet_data': 'choose_dog'}

# обработка команды /start
@bot.message_handler(commands=['start'])
def welcome_message(message):
    # бот предложит юзеру выбрать приют
    bot.send_message(message.chat.id, text=f'Привет! Я бот, который поможет Вам найти четырехлапого друга. Пока я знаю друзей всего в нескольких приютах в Ростове-на-Дону, но скоро их станет больше. Вот где Вы сможете забрать друга домой.', reply_markup=welcome_keyboard()) # показать кнопки

# стартовое меню
def welcome_keyboard():
    buttons = [
        types.InlineKeyboardButton(text='Приют "Зоопомощь"', callback_data='p_zoopomosch'),
        types.InlineKeyboardButton(text='Приют "Котэдж"', callback_data='p_kotedzh'),
        types.InlineKeyboardButton(text='ЗРЦ "Тотошка"', callback_data='zrc_totoshka')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard

# клавиатура для выбора животного
def choose_pet_keyboard():
    buttons = [
        types.InlineKeyboardButton(text='Котика 🐱', callback_data='choose_cat'),
        types.InlineKeyboardButton(text='Пёсика 🐶', callback_data='choose_dog')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

# функция обработки колбэков
@bot.callback_query_handler(func=lambda call: True)
def shelter_callback_query(call):
    shelters_buttons = ['p_zoopomosch', 'p_kotedzh', 'zrc_totoshka']
    pets_buttons = ['choose_cat', 'choose_dog']

    for s in shelters_buttons:
        if call.data == s:
            user_data['shelter_data'] = call.data
            # бот предложит выбрать между кнопками "котик" и "пёсик"
            bot.send_message(call.message.chat.id, text='Кого Вы хотите взять?', reply_markup=choose_pet_keyboard())

    for p in pets_buttons:
        if call.data == p:
            user_data['pet_data'] = call.data

            # открывается соединение с БД
            connect = sqlite3.connect('shelters.db', check_same_thread=False)
            cursor = connect.cursor()

            # если интересуют кошки из п-та "Зоопомощь"
            if user_data == p_zoopomosch_cats:
                cursor.execute(
                    "SELECT petPhoto_src, petName, petDescription, phoneNumber FROM zoopomosch WHERE petCategory = 'Кошка'"
                )
                # сохраним результаты в переменной records
                records = cursor.fetchall()
                # выведем результаты пользователю
                for row in records:
                    pet_photo = open(f'{row[0]}', 'rb')
                    bot.send_photo(
                        call.message.chat.id,
                        photo=pet_photo,
                        caption=f'<b>{row[1]}</b> \n\n{row[2]} \n\n ☎ Телефон: {row[3]}',
                        parse_mode='html'
                    )

            # если интересуют собаки из п-та "Зоопомощь"
            if user_data == p_zoopomosch_dogs:
                cursor.execute(
                    "SELECT petPhoto_src, petName, petDescription, phoneNumber FROM zoopomosch WHERE petCategory = 'Собака'"
                )
                records = cursor.fetchall()
                for row in records:
                    pet_photo = open(f'{row[0]}', 'rb')
                    bot.send_photo(
                        call.message.chat.id,
                        photo=pet_photo,
                        caption=f'<b>{row[1]}</b> \n\n{row[2]} \n\n ☎ Телефон: {row[3]}',
                        parse_mode='html'
                    )

            # кошки п-та "Котэдж"
            if user_data == p_kotedzh_cats:
                cursor.execute(
                    "SELECT petPhoto_src, petName, petDescription, phoneNumber FROM kotedzh WHERE petCategory = 'Кошка'"
                )
                records = cursor.fetchall()
                for row in records:
                    pet_photo = open(f'{row[0]}', 'rb')
                    bot.send_photo(
                        call.message.chat.id,
                        photo=pet_photo,
                        caption=f'<b>{row[1]}</b> \n\n{row[2]} \n\n ☎ Телефон: {row[3]}',
                        parse_mode='html'
                    )

            # собаки п-та "Котэдж"
            if user_data == p_kotedzh_dogs:
                cursor.execute(
                    "SELECT petPhoto_src, petName, petDescription, phoneNumber FROM kotedzh WHERE petCategory = 'Собака'"
                )
                records = cursor.fetchall()
                for row in records:
                    pet_photo = open(f'{row[0]}', 'rb')
                    bot.send_photo(
                        call.message.chat.id,
                        photo=pet_photo,
                        caption=f'<b>{row[1]}</b> \n\n{row[2]} \n\n ☎ Телефон: {row[3]}',
                        parse_mode='html'
                    )

            # кошки ЗРЦ "Тотошка"
            if user_data == zrc_totoshka_cats:
                cursor.execute(
                    "SELECT petPhoto_src, petName, petDescription, phoneNumber FROM zrc_totoshka WHERE petCategory = 'Кошка'"
                )
                records = cursor.fetchall()
                for row in records:
                    pet_photo = open(f'{row[0]}', 'rb')
                    bot.send_photo(
                        call.message.chat.id,
                        photo=pet_photo,
                        caption=f'<b>{row[1]}</b> \n\n{row[2]} \n\n ☎ Телефон: {row[3]}',
                        parse_mode='html'
                    )

            # собаки ЗРЦ "Тотошка"
            if user_data == zrc_totoshka_dogs:
                cursor.execute(
                    "SELECT petPhoto_src, petName, petDescription, phoneNumber FROM zrc_totoshka WHERE petCategory = 'Собака'"
                )
                records = cursor.fetchall()
                for row in records:
                    pet_photo = open(f'{row[0]}', 'rb')
                    bot.send_photo(
                        call.message.chat.id,
                        photo=pet_photo,
                        caption=f'<b>{row[1]}</b> \n\n{row[2]} \n\n Телефон: {row[3]}',
                        parse_mode='html'
                    )

            connect.close()

bot.polling(none_stop=True)