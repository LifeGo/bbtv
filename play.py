#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard imports
import os
import sys
import time
import re
import json

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


def like_url(href):
    if href.strip().startswith('http') and '.' in href:
       return True

    return False


def chk_skip(href):
    domains = [
        'adsco.re',
    ]
    for dm in domains:
       if dm in href:
           return True
    return False


def chk_baloo(href):
    domains = [
        'baloo.co',
    ]
    for dm in domains:
       if dm in href:
           return True
    return False


def wait_second(sec):
    print('wait for {} second ...'.format(sec))
    time.sleep(sec)


def init_webdriver():
    SPROXY = 'socks5://127.0.0.1:1080'
    chrome_options = Options()
    ## chrome_options.add_argument('--headless')
    ## chrome_options.add_argument('--disable-gpu')
    ## chrome_options.add_argument('--no-sandbox')
    ## chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--proxy-server=%s' % SPROXY)
    chrome_options.add_argument('--window-size=1820x980')
    return(webdriver.Chrome(chrome_options=chrome_options))

 
def get_ip_info(webdrv):
    webdrv.set_window_size(1820, 980)
    #webdrv.get('http://baloo.co/episode/pilot-6492562')
    #webdrv.get('http://baloo.co/movie/cadillac-records-1042877')
    webdrv.get('http://baloo.co/movie/candy-jar-6744044')
    main_window = webdrv.current_window_handle

    xpath_s = [
	    '/html/body/div[3]',
	    '//*[@id="at-cv-lightbox-close"]',
	]
    retry = 0
    while retry < 4:
        wait_second(2)
        for xp in xpath_s:
            try:
                webdrv.find_element_by_xpath(xp).click()
                retry += 1
                print('retry ... {}'.format(retry))
            except:
                pass

    xpath_s = [
	    '/html/body/div[3]',
	    '//*[@id="lighty"]/div[2]',
	]
    retry = 0
    while retry < 2:
        wait_second(2)
        for xp in xpath_s:
            try:
                webdrv.find_element_by_xpath(xp).click()
                retry += 1
                print('retry ... {}'.format(retry))
            except:
                pass

    webdrv.switch_to_window(main_window)

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
    wait_second(60)
    exit_web(webdrv)
    sys.exit()
