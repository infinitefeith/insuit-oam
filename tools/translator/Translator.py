from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from retry import retry
import time
import re
from lxml import etree

class Translator():
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=self.chrome_options)

    def __del__(self):
        self.browser.close()

    @retry(tries=1, delay=60)
    def translate(self, input, dest):
        """
        @dest为需要翻译的目标语言
        """
        if input is '' or dest is '':
            return ''
        base_url = 'https://translate.google.cn/?sl=en&tl=%s&op=translate' % dest
        if self.browser.current_url == 'data:,':
            self.browser.get(base_url)
        else:
            local = re.findall(r'&tl=(.*)&text', self.browser.current_url)[0]
            # print(local, dest)
            if local != dest:
                self.browser.get(base_url)
        if len(input) > 2048:
            submit = WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="原文"]')))
            submit.clear()
            submit.send_keys(input)
            # 如果网速慢可以延长等待时间
            time.sleep(1)
        else:
            trans_url = "https://translate.google.cn/?sl=auto&tl=" + dest + "&text=" + input + "&op=translate"
            self.browser.get(trans_url)
        # 下面因为德文某些单词分阴性和阳性所以要再判断一次（不翻德文的可以不用）
        try:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@jsname="W297wb"]')))
            source = etree.HTML(self.browser.page_source)
            #可能设计ZeroWidthSpace, 需要删除
            result = ''.join(source.xpath('//span[@jsname="W297wb"]//text()')).replace('\u200b', '')
        except:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located((By.XPATH, '//span[@jsname="jqKxS"]')))
            source = etree.HTML(self.browser.page_source)
            result = ''.join(source.xpath('//span[@jsname="jqKxS"]//text()')).replace('\u200b', '')

        return result

if __name__ == '__main__':
    t = Translator()
    print(t.translate('中英翻译测试', dest='en'))
    print(t.translate('再测试一下', dest='en'))
    print(t.translate('hello world', dest='zh-CN'))