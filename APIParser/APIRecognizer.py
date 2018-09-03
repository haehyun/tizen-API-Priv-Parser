import re


class getInstance:

    IS_PROLOGUE_READ = False
    IS_PRIVLEVEL_READ = False
    IS_PRIVILEGE_READ = False
    IS_EPILOGUE_READ = False
    IS_NAME_READ = False

    def __init__(self):
        return

    def readPrologue(self, line):
        if "@brief" in line:
            self.IS_PROLOGUE_READ = True

    def readPrivlevel(self, api, line):
        if "@privlevel" in line:
            if "pub" in line:
                api.setPrivlevel("public")
            elif "plat" in line:
                api.setPrivlevel("platform")
            elif "part" in line:
                api.setPrivlevel("partner")
            self.IS_PRIVLEVEL_READ = True


    def readPrivilege(self, api, line):
        if "@privilege" in line:
            if "http://developer.samsung.com/tizen/privilege/" in line:
                result = line.find("http://developer.samsung.com/tizen/privilege/")
                privilege = line[result:]
                privilege = privilege.replace(" ", "")
                privilege = privilege.replace("\t ", "")
                privilege = privilege.replace("\\t ", "")
                privilege = privilege.replace("\n", "")
                privilege = privilege.replace("\\n", "")
                privilege = privilege.rstrip()
                api.addPrivilege(privilege)

            else:
                result = line.find("http://tizen.org")
                privilege = line[result:]
                privilege = privilege.replace(" ", "")
                privilege = privilege.replace("\t ", "")
                privilege = privilege.replace("\\t ", "")
                privilege = privilege.replace("\n", "")
                privilege = privilege.replace("\\n", "")
                privilege = privilege.rstrip()
                api.addPrivilege(privilege)

        elif "@" in line and \
            len(api.getPrivilege()) > 0:
            self.IS_PRIVILEGE_READ = True

        elif "http://tizen.org" in line:
            # print("line:", line.rstrip())
            result = line.find("http://tizen.org")
            privilege = line[result:]
            privilege = privilege.replace(" ", "")
            privilege = privilege.replace("\t ", "")
            privilege = privilege.replace("\\t ", "")
            privilege = privilege.replace("\n", "")
            privilege = privilege.replace("\\n", "")
            privilege = privilege.rstrip()
            api.addPrivilege(privilege)


    def readEpilogue(self, line):
        if "*/" in line:
            self.IS_EPILOGUE_READ = True

    def readName(self, api, line):
        # matchObj = re.match(r'(.*)(\s)(.*)[(](.*)[)](.*)[;]', line, re.M | re.I)
        matchObj = re.match(r'(.*)(\s)(.*)[(]', line, re.M | re.I)
        if matchObj:
            # print(line)
            name = matchObj.group(3)
            if name:
                api.setName(name)
                self.IS_NAME_READ = True


    def reset(self):
        self.IS_PROLOGUE_READ = False
        self.IS_PRIVLEVEL_READ = False
        self.IS_PRIVILEGE_READ = False
        self.IS_EPILOGUE_READ = False
        self.IS_NAME_READ = False

