import telebot
from telebot import types
from config import token


bot = telebot.TeleBot(token)
@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет! Введи вопрос')

@bot.message_handler(content_types=['text'])
def get_user_text(message):
    question = message.text
    clear_question = "".join(filter(lambda x: x == " " or x.isalnum(), question))
    markup = types.InlineKeyboardMarkup()
    like = types.InlineKeyboardButton('LIKE', callback_data='good')
    dislike = types.InlineKeyboardButton('DISLIKE', callback_data='bad')
    markup.add(like, dislike)

    bot.send_message(message.chat.id, f'строка без специальных символов:\n{clear_question}', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

            # remove inline buttons
            bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)

            # show alert
            #bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="notification")

    except Exception as e:
        print(repr(e))
bot.polling(non_stop=True)