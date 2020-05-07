import telebot
import script
from threading import Thread

t = Thread(target = script.scheduler)
t.start()

bot = telebot.TeleBot('Insert your API key')
keyboard = telebot.types.ReplyKeyboardMarkup()
keyboard.row('Начать', 'Помощь')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Здесь ты можешь узнать самую актуальную статистику о распространении '
                                      'COVID-19!', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id,
                     'Просто введи официальное название нужной тебе области, и ты получишь подробную статистику! '
                     'Если бот выдает ошибку, то попробуй убрать или добавить слово типа "республика, область"')


@bot.message_handler(content_types=['text'])
def send_stat(message):
    bot.send_message(message.chat.id, message.text)
    res = script.get_stat_by_name(message.text)
    print('bitch')
    if res:
        print('yeah')
        output = res[0] + '\n' + res[1] + '\n' + res[2] + '\n' + res[3] + '\n'
        bot.send_message(message.chat.id, output)
    else:
        bot.send_message(message.chat.id, 'Неверный ввод')


bot.polling()