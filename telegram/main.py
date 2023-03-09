import telebot


bot = telebot.TeleBot('6290734351:AAGnZaGJCmTXClc0WHdfOTfqnSFb6gOZ1Vs')
@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет! Введи вопрос')

@bot.message_handler()
def get_user_text(message):
    question = message.text
    clear_question_list = []
    for char in question:
        if char == " " or char.isalnum():
            clear_question_list.append(char)
    clear_question = "".join(clear_question_list)
    bot.send_message(message.chat.id, f'строка без специальных символов:\n{clear_question}')

bot.polling(non_stop=True)