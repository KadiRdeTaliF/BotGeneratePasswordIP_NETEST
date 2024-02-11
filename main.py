import telebot
from telebot import  types
import random
import string

bot = telebot.TeleBot('6820027347:AAHFNLY7rbjkHha1XbzKC7hOHcfugRqf3Ps')

len_pass = 0
count_pass = 0
useNumber = bool
useSpecificSymbol = bool

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton('Настройки')
btn2 = types.KeyboardButton('Сгенерировать пароль')
markup.add(btn1,btn2)
btn3 = types.KeyboardButton('Да')
btn4 = types.KeyboardButton('Нет')
markup1.add(btn3, btn4)



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, text='Привет, {0.first_name}! Я крутой бот для генерации паролей.'.format(message.from_user), reply_markup=markup)

@bot.message_handler(commands=['help'])
def start_message1(message):
    bot.send_message(message.chat.id, text='Меня создали лишь с одной целью - генерировать пароли, для настройки пароля тыкните на кнопку настройки'.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Настройки":
        msg = bot.send_message(message.chat.id, text="Хотите ли Вы использовать в вашем пароле цифры?", reply_markup=markup1)
        bot.register_next_step_handler(msg, choose_specifications)
    elif message.text == "Сгенерировать пароль":
        msg = bot.send_message(message.chat.id, 'Сколько паролей Вы хотите сгенерировать? (введите целое число не превышающие 20 и не меньши 0))', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, pass_count)
    else:
        bot.send_message(message.chat.id, 'Извиняюсь, но я такое не умею, напишите /help чтобы посмотреть мой функционал')

@bot.message_handler(content_types='text')
def choose_specifications(message):
    global useNumber
    if message.text == "Да":
        msg = bot.send_message(message.chat.id, 'Хотите ли вы использовать в ваших паролях специальные символы(#@%! и другие)?')
        useNumber = True
        bot.register_next_step_handler(msg, choose_symbols)
    elif message.text == "Нет":
        msg = bot.send_message(message.chat.id, 'Хотите ли вы использовать в ваших паролях специальные символы(#@%! и другие)?')
        useNumber = False
        bot.register_next_step_handler(msg, choose_symbols)
    else:
        bot.send_message(message.chat.id, "Извиняюсь, но я могу принимать в данный момент лишь 2 значение True или False (Да или Нет)")


@bot.message_handler(content_types='text')
def choose_symbols(message):
    global useSpecificSymbol
    if message.text == "Да":
        msg = bot.send_message(message.chat.id, 'Вы успешно настроили бота! Приятной генерации !', reply_markup=markup)
        useSpecificSymbol = True
        bot.register_next_step_handler(msg, message_reply)
    elif message.text == "Нет":
        msg = bot.send_message(message.chat.id, 'Вы успешно настроили бота! Приятной генерации !', reply_markup=markup)
        useSpecificSymbol = False
        bot.register_next_step_handler(msg, message_reply)
    else:
        bot.send_message(message.chat.id,"Извиняюсь, но я могу принимать в данный момент лишь 2 значение True или False (Да или Нет)", reply_markup=markup)


@bot.message_handler(content_types='text')
def pass_count(message):
    global count_pass
    try:
        count_pass = int(message.text)
        if 0 < count_pass <= 20:
            msg = bot.send_message(message.chat.id, 'Какой длины вы хотите пароль? (введите число не привышающие 30 и не меньши 0)')
            bot.register_next_step_handler(msg, pass_len)
        else:
            bot.send_message(message.chat.id, 'Слишком большое число(', reply_markup=markup)
    except:
        bot.send_message(message.chat.id, 'Введите число не больше 20', reply_markup=markup)

@bot.message_handler(content_types='text')
def pass_len(message):
    global len_pass
    try:
        len_pass = int(message.text)
        if useSpecificSymbol and useNumber == True:
            if 0 < len_pass <= 30:
                for j in range(count_pass):
                    passwords = ''
                    for i in range(len_pass):
                        passwords += random.choice(string.ascii_letters + string.digits + string.punctuation)
                    bot.send_message(message.chat.id, passwords, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Введите целое число не больше 30 и больше 0', reply_markup=markup)
        elif useSpecificSymbol == True and useNumber == False:
            if 0 < len_pass <= 30:
                for j in range(count_pass):
                    passwords = ''
                    for i in range(len_pass):
                        passwords += random.choice(string.ascii_letters + string.punctuation)
                    bot.send_message(message.chat.id, passwords, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Введите целое число не больше 30 и больше 0', reply_markup=markup)
        elif useSpecificSymbol == False and useNumber == True:
            if 0 < len_pass <= 30:
                for j in range(count_pass):
                    passwords = ''
                    for i in range(len_pass):
                        passwords += random.choice(string.ascii_letters + string.digits)
                    bot.send_message(message.chat.id, passwords, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Введите целое число не больше 30 и больше 0', reply_markup=markup)
        else:
            if 0 < len_pass <= 30:
                for j in range(count_pass):
                    passwords = ''
                    for i in range(len_pass):
                        passwords += random.choice(string.ascii_letters)
                    bot.send_message(message.chat.id, passwords, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, 'Введите целое число не больше 30 и больше 0', reply_markup=markup)
    except:
        bot.send_message(message.chat, 'Введите целое число не больше 30', reply_markup=markup)

bot.polling(non_stop=True)


# if 0 < len_pass <= 30:
#     l = len_pass
#     c = count_pass
#     passwords = ''
#     for i in range(c):
#         passwords = ''
#         for j in range(l):
#             passwords += random.choice(chars)
#         passwords += passwords + '\n'
#     bot.send_message(message.chat.id, passwords, reply_markup=markup)
# else:
#     bot.send_message(message.chat.id, 'Вы ввели некорректное число', reply_markup=markup)
# except:
# bot.send_message(message.chat, 'Введите целое число не больше 30', reply_markup=markup)
# @bot.message_handler(content_types=['Создать пароль/пароли'])
# def gen_pas(message):
#     longpas = types.InlineKeyboardMarkup()
#     longpas.add(types.InlineKeyboardMarkup(''))
#     bot.reply_to(message, "")
#
# @bot.message_handler(commands=['start'])
# def main(message):
#     bot.send_message(message.chat.id , 'Привет! Я существую лишь с одной целью - генерации паролей')
