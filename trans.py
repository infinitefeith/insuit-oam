import sys
import os
from tools.translator.Translator import *
from tools.rfctranslator import rfcTranslate

if __name__ == "__main__":
    g = os.walk(r"./drafts")
    google = Translator()
    for path, dir_list, file_list in g:
        for file_name in file_list:
            filepath = os.path.join(path, file_name)
            print("processing file: %s " % filepath)
            rfcTranslate(google, filepath, filepath.replace('.txt', '_CN.txt'))