import telebot
from telebot import types
from config import token
from firebaseDataStore.main import DatabaseHelper
from model import AnsweringModel
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(token)
helper = DatabaseHelper()
data = {}
year = 0

#model = AnsweringModel("config.yaml")


@bot.message_handler(commands=['start'])
def start(message):
    logger.info(message.from_user.id)
    markup_year = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton('1️⃣', callback_data='1')
    two = types.InlineKeyboardButton('2️⃣', callback_data='2')
    three = types.InlineKeyboardButton('3️⃣', callback_data='3')
    four = types.InlineKeyboardButton('4️⃣', callback_data='4')
    five = types.InlineKeyboardButton('5️⃣', callback_data='5')
    six = types.InlineKeyboardButton('6️⃣', callback_data='6')

    # markup_subject = types.InlineKeyboardMarkup()
    # programming = types.InlineKeyboardButton('1️⃣', callback_data='1')
    # informatics = types.InlineKeyboardButton('2️⃣', callback_data='2')
    # oop = types.InlineKeyboardButton('3️⃣', callback_data='3')
    # aisd = types.InlineKeyboardButton('4️⃣', callback_data='4')
    # piaa = types.InlineKeyboardButton('5️⃣', callback_data='5')
    # bd = types.InlineKeyboardButton('6️⃣', callback_data='6')
    # oprpo = types.InlineKeyboardButton('3️⃣', callback_data='3')
    # testing = types.InlineKeyboardButton('4️⃣', callback_data='4')
    # neural_networks = types.InlineKeyboardButton('5️⃣', callback_data='5')
    # bz = types.InlineKeyboardButton('6️⃣', callback_data='6')

    markup_year.add(one, two, three, four, five, six)
    bot.send_message(message.chat.id, "Привет! Укажи свой номер курса\nИли можете начать сначала: /start",
                     reply_markup=markup_year)
    # bot.send_message(message.chat.id,"А также предмет по которому хочешь задать вопрос\nИли можете начать сначала: /start", reply_markup = markup_subject)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    logger.info("get_message")
    if year == 0:
        bot.send_message(message.chat.id, "Вы не выбрали курс!")
    else:
        data.clear()
        question = message.text
        clear_question = "".join(filter(lambda x: x == " " or x.isalnum(), question))
        markup = types.InlineKeyboardMarkup()
        like = types.InlineKeyboardButton('LIKE👍', callback_data='good')
        dislike = types.InlineKeyboardButton('DISLIKE👎', callback_data='bad')
        markup.add(like, dislike)
        logger.info(f'номер курса {year}')
        #answer = model.get_answer(clear_question, year, 'subject')
        answer = "ANSWER"
        data['question'] = clear_question
        data['answer'] = answer
        bot.send_message(message.chat.id, answer, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global year
    if call.message:
        if call.data == 'good':
            bot.send_message(call.message.chat.id, 'Вот и отличненько 😊\nМожете начать сначала: /start')
            if len(data.keys()) == 2:
                helper.like(data)
                data.clear()
        elif call.data == 'bad':
            bot.send_message(call.message.chat.id, 'Бывает 😢\nМожете начать сначала: /start')
            if len(data.keys()) == 2:
                helper.dislike(data)
                data.clear()
        else:
            year = int(call.data)
            logger.info(f'номер курса {year}')
            bot.send_message(call.message.chat.id,
                             'Теперь можете задать вопрос\nИли можете начать сначала: /start')
        # remove inline buttons
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)



bot.polling(non_stop=True)
