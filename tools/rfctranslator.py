#-*- coding:utf-8 -*-
import sys
import os
import re
import textwrap
from tools.translator.Translator import Translator

def isFilePath(path):
    """
    检查是否为文件路径
    :param path:
    :return:
    """
    prog = re.compile("[a-zA-Z]:\\((?:[a-zA-Z0-9() ]*\\)*).*")
    result = prog.match(path)
    if os.path.isfile(path) or result:
        return True
    else:
        return False

def sectionFormat(str):
    """
    段落格式化
    :param str:
    :return:
    """
    if str is '':
        return ''
    # 假设字符串不是{数字.}开头，自动首行缩进
    if not re.match('^[0-9]*\.', str):
        str = '  ' + str
    # 按照行宽度换行使用
    str = textwrap.fill(str, width=40)
    return str

def getPrefixAndContent(line):
    """
    获取前缀和内容
    :param line:
    :return:
    """
    if ':' not in line:
        return '', line
    temp = line.split(':', maxsplit=1)
    if len(temp[0]) > 30:
        return '', line
    else:
        prefix = temp[0]
        line = temp[1]
    return prefix, line

def isFigure(section):
    """
    检查是否为图表
    :param section:
    :return:
    """
    pattern = ['+-+-+', '------', '======', '.....']
    # 遍历图标的特征并在段落中查询
    for p in pattern:
        if p in section:
            return True
    return False

def isNotTrans(section):
    """
    检查是否需要转换
    :param section:
    :return:
    """
    pattern = ['^\[RFC', '^\[I-D']
    for p in pattern:
        if re.match(p, section):
            return True

    pattern2 = ['[Page ', ". . . "]
    for p in pattern2:
        if p in section:
            return True
    return False

def rfcTranslate(translator, srcfilename, dstfilename):
    """
    :param srcfilename:
    :param dstfilename:
    :return:
    """
    if srcfilename is '' or dstfilename is '':
        return
    dscfile = open(dstfilename, "w+", encoding='utf-8')
    with open(srcfilename, "r+") as srcfile:
        content = srcfile.read()
        # 按段分割文件
        segments = content.split("\n\n")
        # 遍历段并翻译
        for section in segments:
            # 当前段是图标段 或者 当前段是目录段
            if isFigure(section) or isNotTrans(section):
                # print(section)
                sectionflag = True
            # 当前段是内容段
            else:
                line = ' '.join(section.replace("\n", "").split())
                print(line)
                if line is not '':
                    prefix, line = getPrefixAndContent(line)
                    transline = translator.translate(line, dest='zh-CN')
                    if prefix is not '':
                        transline = "{prefix} : {content}".format(prefix=prefix, content=transline)
                    transline = sectionFormat(transline)
                    print(transline)

                sectionflag = False

            #写文档
            if sectionflag is True:
                dscfile.write(section)
            elif line is not '':
                dscfile.write(transline)
            dscfile.write("\n\n")
    dscfile.close()

if __name__ == "__main__":
    # 创建翻译器
    google = Translator()
    rfcTranslate(google, 'draft-varga-detnet-service-sub-layer-oam-03.txt', 'draft-varga-detnet-service-sub-layer-oam-03_CN.txt')