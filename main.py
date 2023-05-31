import telebot
from telebot import types
from config import token
from firebaseDataStore.main import DatabaseHelper
from model import AnsweringModel
from firebaseDataStore.dataAdministrator import DataAdministrator
from scripts.create_link_manifest import create_link_manifest
import logging
import argparse
from hyperpyyaml import load_hyperpyyaml
import urllib3

import sched, time

class Links:
    def __init__(self):
        self.link_manifest = create_link_manifest("https://se.moevm.info")
        self.s = sched.scheduler(time.time, time.sleep)

    def update_link_manifest(self):
        self.s.enter(60, 1, self.update_link_manifest())
        self.link_manifest = create_link_manifest("https://se.moevm.info")
        logger.info("SASAT'")

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

bot = telebot.TeleBot(token)
helper = DatabaseHelper()
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)

    args = parser.parse_args()

    with open(args.config) as f:
        config_yaml = f.read()
    config = load_hyperpyyaml(config_yaml)

# model = AnsweringModel(config)

dataAdmin = DataAdministrator()
links_manifest = Links()
links_manifest.s.run()
logger.info("finish create_link_manifest")


@bot.message_handler(commands=['start'])
def start(message):
    logger.info(message.from_user.id)
    dataAdmin.delUserInfo(message.from_user.id)
    dataAdmin.addUser(message.from_user.id)
    markup_year = types.InlineKeyboardMarkup()
    one = types.InlineKeyboardButton('1️⃣', callback_data='1')
    two = types.InlineKeyboardButton('2️⃣', callback_data='2')
    three = types.InlineKeyboardButton('3️⃣', callback_data='3')
    four = types.InlineKeyboardButton('4️⃣', callback_data='4')
    five = types.InlineKeyboardButton('5️⃣', callback_data='5')
    six = types.InlineKeyboardButton('6️⃣', callback_data='6')

    markup_year.add(one, two, three, four, five, six)
    bot.send_message(message.chat.id, "Привет! Укажи свой номер курса\nИли можете начать сначала: /start",
                     reply_markup=markup_year)
    # bot.send_message(message.chat.id,"А также предмет по которому хочешь задать вопрос\nИли можете начать сначала: /start", reply_markup = markup_subject)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    logger.info("get_message")
    logger.info(message.from_user.id)
    _id = message.from_user.id
    dataAdmin.addUser(_id)
    if dataAdmin.yearForCurrentId(_id) == 0:
        bot.send_message(message.chat.id, "Вы не выбрали курс! Выберете сверху или нажмите /start")

    elif dataAdmin.subjectForCurrentId(_id) == 0:
        list_subjects = list(set(
            [j["subject"] for j in links_manifest.link_manifest if j["num_course"] == dataAdmin.yearForCurrentId(_id)]))

        if message.text.isdigit() and 1 <= int(message.text) <= len(list_subjects):
            nub_subject = int(message.text) - 1
            subject = list_subjects[nub_subject]
            bot.send_message(message.chat.id, "Вы выбрали предмет: " +
            subject +"\nТеперь можете задать свой вопрос по этому предмету\nИли можете начать сначала /start")
            logger.info(subject)
            dataAdmin.addInfo(_id, 'subject', subject)
            logger.info(dataAdmin.subjectForCurrentId(_id))
        else:
            bot.send_message(message.chat.id, "Введите нужное число!")

    else:
        question = message.text
        clear_question = "".join(filter(lambda x: x == " " or x.isalnum(), question))
        markup = types.InlineKeyboardMarkup()
        like = types.InlineKeyboardButton('LIKE👍', callback_data='good')
        dislike = types.InlineKeyboardButton('DISLIKE👎', callback_data='bad')
        markup.add(like, dislike)
        logger.info(f'номер курса {dataAdmin.yearForCurrentId(_id)}')
        logger.info(dataAdmin.getDataForUser(_id))
        answer = "ANSWER"
        # answer = model.get_answer(clear_question, dataAdmin.yearForCurrentId(_id), dataAdmin.subjectForCurrentId(_id))
        dataAdmin.addInfo(_id, 'question', clear_question)
        dataAdmin.addInfo(_id, 'answer', answer)
        bot.send_message(message.chat.id, answer, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    logger.info(call.from_user.id)
    if call.message:
        _id = call.from_user.id
        if call.data == 'good':
            bot.send_message(call.message.chat.id, 'Вот и отличненько 😊\nМожете начать сначала: /start')
            if dataAdmin.checkIfPossibleForReaction(_id):
                helper.like(dataAdmin.getDataForUser(_id))
                logger.info(dataAdmin.getDataForUser(_id))
                dataAdmin.delUserInfo(_id)
        elif call.data == 'bad':
            bot.send_message(call.message.chat.id, 'Бывает 😢\nМожете начать сначала: /start')
            if dataAdmin.checkIfPossibleForReaction(_id):
                helper.dislike(dataAdmin.getDataForUser(_id))
                logger.info(dataAdmin.getDataForUser(_id))
                dataAdmin.delUserInfo(_id)
        else:
            year = int(call.data)
            dataAdmin.addUser(_id)
            dataAdmin.addInfo(_id, 'year', year)
            logger.info(f'номер курса {year}')
            list_subjects = list(set([j["subject"] for j in links_manifest.link_manifest if j["num_course"] == year]))
            numbered_list_subjects = []
            for i in range(len(list_subjects)):
                numbered_list_subjects.append(str(i + 1) + ") " + list_subjects[i])

            bot.send_message(call.message.chat.id,
                             "Выбери интересующий предмет, для это отпрвьте число от 1 до " +
                             str(len(numbered_list_subjects)) + ":\n" +
                             "\n".join(numbered_list_subjects) + "\nИли можете начать сначала: /start")
        # remove inline buttons
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id)


bot.polling(non_stop=True)
