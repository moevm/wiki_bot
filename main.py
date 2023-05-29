import telebot
from telebot import types
from config import token
from firebaseDataStore.main import DatabaseHelper
from model import AnsweringModel
from firebaseDataStore.dataAdministrator import DataAdministrator
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

bot = telebot.TeleBot(token)
helper = DatabaseHelper()

year = 0

# model = AnsweringModel("config.yaml")

dataAdmin = DataAdministrator()


@bot.message_handler(commands=['start'])
def start(message):
    logger.info(message.from_user.id)
    dataAdmin.addUser(message.from_user.id)
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
    _id = message.from_user.id
    dataAdmin.addUser(_id)
    if dataAdmin.yearForCurrentId(_id) == 0:
        bot.send_message(message.chat.id, "Вы не выбрали курс!")
    else:
        dataAdmin.delUserInfo(message.from_user.id)
        question = message.text
        clear_question = "".join(filter(lambda x: x == " " or x.isalnum(), question))
        markup = types.InlineKeyboardMarkup()
        like = types.InlineKeyboardButton('LIKE👍', callback_data='good')
        dislike = types.InlineKeyboardButton('DISLIKE👎', callback_data='bad')
        markup.add(like, dislike)
        logger.info(f'номер курса {year}')
        # answer = model.get_answer(clear_question, year, 'subject')
        answer = "ANSWER"
        dataAdmin.addInfo(_id, 'question', clear_question)
        dataAdmin.addInfo(_id, 'answer', answer)
        bot.send_message(message.chat.id, answer, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global year
    if call.message:
        _id = call.from_user.id
        if call.data == 'good':
            bot.send_message(call.message.chat.id, 'Вот и отличненько 😊\nМожете начать сначала: /start')
            if dataAdmin.checkIfPossibleForReaction(_id):
                helper.like(dataAdmin.getDataForUser(_id))
                dataAdmin.delUserInfo(_id)
        elif call.data == 'bad':
            bot.send_message(call.message.chat.id, 'Бывает 😢\nМожете начать сначала: /start')
            if dataAdmin.checkIfPossibleForReaction(_id):
                helper.dislike(dataAdmin.getDataForUser(_id))
                dataAdmin.delUserInfo(_id)
        else:
            year = int(call.data)
            dataAdmin.addUser(_id)
            dataAdmin.addInfo(_id, 'year', year)
            logger.info(f'номер курса {year}')
            bot.send_message(call.message.chat.id,
                             'Теперь можете задать вопрос\nИли можете начать сначала: /start')
        # remove inline buttons
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)


bot.polling(non_stop=True)
