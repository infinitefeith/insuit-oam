import sys

from translator.Translator import Translator

if __name__ == "__main__":
    google = Translator()
    dscfile = open("rfc8321-1.txt", "w+")
    with open("rfc8321.txt", "r+") as srcfile:
        content = srcfile.read()
        segments = content.split("\n\n")
        for section in segments:
            #当前段是图标段
            if "------" in section or "======" in section:
                print(section)
                psection = True
            #当前段是目录段
            elif ". . . . ." in section:
                print(section)
                psection = True
            #当前段是页头
            elif "[Page " in section:
                print(section)
                psection = True
            #当前段是内容段
            else:
                line = ' '.join(section.replace("\n", "").split())
                print(line)
                psection = False
                if line is not '':
                    linde = google.translate(line, dest='zh-CN')

            if psection is True:
                dscfile.write(section)
            else:
                dscfile.write(line)
            dscfile.write("\n")
    dscfile.close()
