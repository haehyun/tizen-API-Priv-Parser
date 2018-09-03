
class getInstance:
    'Model class for Tizen API'


    def __init__(self):
        self.privlevel = ""
        self.privilege = list()
        self.name = ""


    def setPrivlevel(self, privlevel):
        self.privlevel = privlevel

    def addPrivilege(self, privilege):
        self.privilege.append(privilege)
        self.privilege.sort()

    def setName(self, name):
        self.name = name


    def getPrivlevel(self):
        return self.privlevel

    def getPrivilege(self):
        return self.privilege

    def getName(self):
        return self.name

    def display(self):
        print("============================================")
        print("Privlevel : ", self.privlevel)
        print("Privilege : ", self.privilege)
        print("name : ", self.name)
        print("============================================\n")


