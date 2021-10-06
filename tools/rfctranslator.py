import sys
import os
import re
import textwrap
from translator.Translator import Translator

def isFilePath(path):
    prog = re.compile("[a-zA-Z]:\\((?:[a-zA-Z0-9() ]*\\)*).*")
    result = prog.match(path)
    if os.path.isfile(path) or result:
        return True
    else:
        return False

def sectionFormat(str):
    if str is '':
        return ''
    #假设字符串不是{数字.}开头，自动首行缩进
    if not re.match('^[0-9]*\.', str):
        str = '  ' + str
    # 按照行宽度换行使用
    str = textwrap.fill(str, width=40)
    return str

def rfcTranslate(srcfilename, dstfilename):

    if srcfilename is '' or dstfilename is '':
        return
    #创建翻译器
    google = Translator()
    dscfile = open(dstfilename, "w+")
    with open(srcfilename, "r+") as srcfile:
        content = srcfile.read()
        #按段分割文件
        segments = content.split("\n\n")
        #遍历段并翻译
        for section in segments:
            #当前段是图标段
            if "------" in section or "======" in section:
                # print(section)
                sectionflag = True
            #当前段是目录段
            elif ". . . . ." in section:
                # print(section)
                sectionflag = True
            #当前段是页头
            elif "[Page " in section:
                # print(section)
                sectionflag = True
            #当前段是内容段
            else:
                line = ' '.join(section.replace("\n", "").split())
                print(line)
                sectionflag = False
                if line is not '':
                    transline = google.translate(line, dest='zh-CN')
                    transline = sectionFormat(transline)
                    print(transline)
            
            if sectionflag is True:
                dscfile.write(section)
            elif line is not '':
                dscfile.write(transline)
            dscfile.write("\n\n")
    dscfile.close()

if __name__ == "__main__":
    rfcTranslate('rfc8321.txt', 'rfc8321_trans.txt')