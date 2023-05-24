import firebase_admin
from firebase_admin import db
import json





class DatabaseHelper:

    def __init__(self):
        self.cred_object = firebase_admin.credentials.Certificate('./key/certFirebase.json')
        self.default_app = firebase_admin.initialize_app(self.cred_object, {
            'databaseURL': "https://wiki-bot-56d5c-default-rtdb.europe-west1.firebasedatabase.app/"
        })
        self.ref = db.reference("/")

    def like(self, data):
        '''
        :param data: dictionary like: {
            'question':question_value
            'answer': answer_value
        }
        :return: nothing
        '''

        newData = data
        newData["reaction"] = "good"
        jsonData = json.dumps(newData)

        self.ref.push(jsonData)




    def dislike(self, data):
        '''
                :param data: dictionary like: {
                    'question':question_value
                    'answer': answer_value
                }
                :return: nothing
                '''

        newData = data
        newData["reaction"] = "bad"
        jsonData = json.dumps(newData)

        self.ref.push(jsonData)
