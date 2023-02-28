import telebot
import re
bot = telebot.TeleBot('6290734351:AAGnZaGJCmTXClc0WHdfOTfqnSFb6gOZ1Vs')

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет! Введи вопрос')

@bot.message_handler()
def get_user_text(message):
    question = message.text
    clear_question = re.sub('[~|`|!|@|#|$|%|^|&|*|(|)|-|_|+|=|{|}|[|\|/]','',question)

    bot.send_message(message.chat.id, 'строка без специальных символов: '+ clear_question)


bot.polling(non_stop=True)


