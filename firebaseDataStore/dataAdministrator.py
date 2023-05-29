class DataAdministrator:
    def __init__(self):
        self.data = {}

    def addUser(self, _id):
        if len(list(self.data[_id].keys()))==0:
            self.data[_id] = {}

    def addInfo(self, _id, key, value):
        self.data[_id][key] = value

    def delUserInfo(self, _id):
        self.data[_id].clear()

    def checkIfPossibleForReaction(self, _id):
        l = list(self.data[_id].keys())
        return True if l.count('question')!=0 and l.count('answer')!=0 else False

    def getDataForUser(self, _id):
        return self.data[_id]


