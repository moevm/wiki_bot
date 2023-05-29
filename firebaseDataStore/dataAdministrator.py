class DataAdministrator:
    def __init__(self):
        self.data = {}

    def addUser(self, id):
        self.data[id] = {}

    def addInfo(self, id, key, value):
        self.data["id"][key] = value
