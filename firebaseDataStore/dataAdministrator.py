class DataAdministrator:
    def __init__(self):
        self.data = {}

    def addUser(self, _id):
        if list(self.data.keys()).count(_id)==0:
            self.data[_id] = {}

    def addInfo(self, _id, key, value):
        self.data[_id][key] = value

    def delUserInfo(self, _id):
        try:
            self.data[_id].clear()
        except:
            print("No such user")

    def yearForCurrentId(self, _id):
        try:
            return self.data[_id]["year"]
        except:
            return 0

    def subjectForCurrentId(self, _id):
        try:
            return self.data[_id]["subject"]
        except:
            return 0

    def checkIfPossibleForReaction(self, _id):
        l = list(self.data[_id].keys())
        return True if l.count('question')!=0 and l.count('answer')!=0 else False

    def getDataForUser(self, _id):
        return self.data[_id]


