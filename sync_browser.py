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

base_dir = ''
site_url = 'http://www.baloo.co'
site_path = ''

visited_links = []
error_links = []
run_log = []

def log_pr(_log):
    global run_log
    run_log.append(str(_log))
    print(str(_log))

def log_save(_flog):
    with open(_flog, 'w', encoding='utf-8') as fp:
        try:
            for _log in run_log:
                fp.write('{}\n'.format(_log))
            fp.close()
        except:
            pass

def init_env():
    global base_dir
    global site_url
    global site_path
    try:
        base_dir = os.getcwd()
        site_url = sys.argv[1]
        site_path = sys.argv[2]
        if not site_url.endswith('/'):
            site_url += '/'
        if not site_path.endswith('/'):
            site_path += '/'
        os.makedirs(site_path, exist_ok=True)

    except IndexError:
        print('Usage:\npython app.py www.example.com folder_name')
        sys.exit(1)


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
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--proxy-server=%s' % SPROXY)
    chrome_options.add_argument('--window-size=1820x980')
    return(webdriver.Chrome(chrome_options=chrome_options))

 
def get_ip_info(webdrv):
    webdrv.set_window_size(1820, 980)
    webdrv.get('http://www.baloo.co')
    wait_second(20)
    timings = webdrv.execute_script("return window.performance.getEntries();")
    json_txt = json.dumps(timings, sort_keys=True, indent=4, separators=(',', ': '))

    html_id = 0
    with open('json_%d.txt' % (html_id), 'w', encoding='utf-8') as fp:
        try:
            fp.write(str(json_txt))
            fp.close()
        except:
            pass

    html = webdrv.page_source
    ##html = webdrv.page_source
    ##json_text = BeautifulSoup(html, 'lxml').get_text()
    ##json_crash = json.loads(json_text)
    with open('video_%d.html' % (html_id), 'w', encoding='utf-8') as fp:
        try:
            _pretty = BeautifulSoup(html, 'lxml').prettify()
            fp.write(str(_pretty))
            fp.close()
        except:
            pass

def exit_web(webdrv):
    webdrv.quit()

def crawl(webdrv, link):
    global site_url
    global visited_links

    if not like_url(link) or chk_skip(link) or not chk_baloo(link):
        print('---: {}'.format(link))
        return()

    #if site_url in link and link not in visited_links:
    if link not in visited_links:
        log_pr('+++: {}'.format(link))
        #print('+++: {}'.format(link))
        visited_links.append(link)

        if 'http://baloo.co/admin/covers/' in link:
            print('0. Working with : {} >>> JPG'.format(link))
            return()
        elif link.lower().endswith('.pdf'):
            print('0. Working with : {} >>> PDF'.format(link))
            return()
        elif link.lower().endswith('.zip'):
            print('0. Working with : {} >>> ZIP'.format(link))
            return()
        elif link.lower().endswith('.jpg'):
            print('0. Working with : {} >>> JPG'.format(link))
            return()
        elif link.lower().endswith('.png'):
            print('0. Working with : {} >>> PNG'.format(link))
            return()
        elif link.lower().endswith('.gif'):
            print('0. Working with : {} >>> GIF'.format(link))
            return()
        elif link.lower().endswith('.apk'):
            print('0. Working with : {} >>> APK'.format(link))
            return()

        webdrv.get(link)
        html = webdrv.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            _url = link.get('href')

            if chk_skip(_url) or '-' in _url:
                log_pr('---: {}'.format(_url))
                #print('---: {}'.format(_url))
                continue

            m_url = _url
            if not like_url(_url):
                if not _url.startswith('/'):
                    _url = site_url + '/' + _url 
                else:
                    _url = site_url + _url
            #print('HREF: {} => {}'.format(m_url, _url))

            if chk_baloo(_url):
                crawl(webdrv, _url)


def gogo(webdrv):
    webdrv.set_window_size(1820, 980)
    crawl(webdrv, site_url)
    return()
    webdrv.get('http://www.baloo.co')
    wait_second(2)

    timings = webdrv.execute_script("return window.performance.getEntries();")
    json_txt = json.dumps(timings, sort_keys=True, indent=4, separators=(',', ': '))
    for tim in timings:
        _url = tim["name"]
        if chk_baloo(_url):
            print('_URL00: {}'.format(tim["name"]))
            crawl(webdrv, _url)
        else:
            print('---: {}'.format(tim["name"]))

    print('Link crawled\n')
    for link in visited_links:
        print('--- {}'.format(link))
    
    print('\n\nLink error\n')
    for link in error_links:
        print('--- {}'.format(link))

if __name__=='__main__':
    #init_env()
    webdrv = init_webdriver()
    #get_ip_info(webdrv)
    gogo(webdrv)
    wait_second(60)
    exit_web(webdrv)
    log_save('run.log')
    sys.exit()
