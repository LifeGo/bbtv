#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard imports
import sys
import time
import re
import json

from selenium import webdriver
from bs4 import BeautifulSoup
from pyvirtualdisplay import Display
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def wait_second(sec):
    print('wait for {} second ...'.format(sec))
    time.sleep(sec)


def init_webdriver():
    SPROXY = 'socks5://127.0.0.1:1080'
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--proxy-server=%s' % SPROXY)
    chrome_options.add_argument('--window-size=1920x1080')
    return(webdriver.Chrome(chrome_options=chrome_options))

 
def get_ip_info(webdrv):
    webdrv.get('http://www.flowyourvideo.com/embed/5b18bcb235d9e')
    wait_second(20)
    timings = webdrv.execute_script("return window.performance.getEntries();")
    #print(timings)
    json_txt = json.dumps(timings, sort_keys=True, indent=4, separators=(',', ': '))
    print(json_txt)
    html_id = 0
    with open('json_%d.html' % (html_id), 'w', encoding='utf-8') as fp:
        try:
            fp.write(str(json_txt))
            fp.close()
        except:
            pass

    html = webdrv.page_source
    html_id = 0
    with open('video_%d.html' % (html_id), 'w', encoding='utf-8') as fp:
        try:
            _pretty = BeautifulSoup(html, 'lxml').prettify()
            fp.write(str(_pretty))
            fp.close()
        except:
            pass

def exit_web(webdrv):
    webdrv.quit()


if __name__=='__main__':
    webdrv = init_webdriver()
    get_ip_info(webdrv)
    exit_web(webdrv)
    sys.exit()
