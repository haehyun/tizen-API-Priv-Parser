import tkinter as tk
from tkinter import filedialog
import os
import re
from openpyxl import Workbook

import TizenAPI
import APIRecognizer
import XLManager

root = tk.Tk()
root.withdraw()
path = filedialog.askdirectory()
#path = "/home/hcho/tizen-full-mobile/platform"

# Create a model instance of the Tizen API
api = TizenAPI.getInstance()
apiRecognizer = APIRecognizer.getInstance()
xlManager = XLManager.getInstance()

# Recursively visit the target directory
for root, subFolders, files in os.walk(path):
    for f in files:

        # Pattern matching for .h files
        #m = re.search("[.][ch]", f)

        if str(f).endswith(".c") \
            or str(f).endswith(".h") :
            # Open source code files
            with open(os.path.join(root, f), 'r', encoding="ISO-8859-1") as fin:

                # Check source code lines
                for line in fin:
                    # print("line : ", line)

                    if not apiRecognizer.IS_PROLOGUE_READ:
                        # print("raed Prologue")
                        apiRecognizer.readPrologue(line)

                    elif apiRecognizer.IS_PROLOGUE_READ and \
                        not apiRecognizer.IS_PRIVLEVEL_READ:
                        # print("raed Privlevel")
                        apiRecognizer.readPrivlevel(api, line)

                    elif apiRecognizer.IS_PRIVLEVEL_READ and \
                        not apiRecognizer.IS_PRIVILEGE_READ:
                        # print("raed Privilege")
                        apiRecognizer.readPrivilege(api, line)

                    elif apiRecognizer.IS_PRIVILEGE_READ and \
                        not apiRecognizer.IS_EPILOGUE_READ:
                        # print("raed Epulogue")
                        apiRecognizer.readEpilogue(line)

                    elif apiRecognizer.IS_EPILOGUE_READ and \
                        not apiRecognizer.IS_NAME_READ:
                        # print("raed Name")
                        apiRecognizer.readName(api, line)

                    elif apiRecognizer.IS_NAME_READ:
                        api.display()
                        xlManager.writeAPI(api)
                        apiRecognizer.reset()
                        api = TizenAPI.getInstance()

                    elif not apiRecognizer.IS_NAME_READ and \
                                    "/**" in line:
                        apiRecognizer.reset()

xlManager.save(path)

