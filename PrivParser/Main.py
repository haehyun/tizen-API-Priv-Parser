import tkinter as tk
from tkinter import filedialog
import os
import re
from openpyxl import Workbook

import XLManager

# import pdb
# pdb.set_trace()

root = tk.Tk()
root.withdraw()
path = filedialog.askdirectory()
#path = "/home/hcho/tizen-full-mobile/platform"

xlManager = XLManager.getInstance()

exclusion_list = ["static", "EXPORT_API", "INTERNAL_FUNC", "TPL_API", "inline", "typedef"]

func_list = []
priv_list = []

start_comment = 0;
exclusion = 0;

# Recursively visit the target directory
for root, subFolders, files in os.walk(path):
    for f in files:

        if str(f).endswith(".c") \
            or str(f).endswith(".h") :
            # Open source code files
            with open(os.path.join(root, f), 'r', encoding="ISO-8859-1") as fin:
                pattern = re.compile(r'(?!\b(if|while|for|switch)\b)\b\w+(?=\s*\()')
                # Check source code lines
                for line in fin:
                    exclusion = 0
                    
                    if "/*" in line:
                        start_comment = 1

                    if "*/" in line:
                        start_comment = 0

                    for x in exclusion_list:
                        if x in line:
                            exclusion = 1
                            break

                    if start_comment == 0 and exclusion == 0 :
                        matches = pattern.finditer(line)
                        for matchNum, match in enumerate(matches):
                            matchNum = matchNum + 1
                            exclusion = 0

                            if "//" in line:
                                sc = line.split("//")
                                if match.group() in sc[1]:
                                    exclusion = 1

                            if "\"" in line:
                                sc = line.split("\"")
                                for x in range(1, len(sc)):
                                    if match.group() in sc[x]:
                                        exclusion = 1

                            if "#define" in line:
                                sc = line.split(" ")
                                if match.group() in sc[1]:
                                    exclusion = 1

                            if exclusion == 0:
                                # print("Match!: {match}".format(match = match.group()))
                                if (match.group() in func_list) == False :
                                    func_list.append(match.group())
                             
xlManager.writeXL(func_list, len(func_list), "func")
xlManager.readXL("func")
xlManager.save(path)