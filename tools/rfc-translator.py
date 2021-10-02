import sys

from translator.Google import GoogleTranslate

if __name__ == "__main__":
    google = GoogleTranslate()
    # dscfile = open("rfc8321-1.txt", "w+")
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
                print(google.translate('en', 'zh', line))

    #         if psection is True:
    #             dscfile.write(section)
    #         else:
    #             dscfile.write(line)
    #         dscfile.write("\n")
    # dscfile.close()
