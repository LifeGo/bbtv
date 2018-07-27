#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard imports
import os
import sys
import time
import re
import json

from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

site_url = 'http://www.baloo.co'
seek_urls = [
    'http://www.baloo.co/movies',
    'http://www.baloo.co/tvseries',
    'http://www.baloo.co/genre',
]


def like_url(href):
    if href is None:
        return False

    if href.strip().startswith('http') and '.' in href:
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
    chrome_options.add_argument('--window-size=1280x640')
    return(webdriver.Chrome(chrome_options=chrome_options))

 
def get_mv_list(webdrv, url):
    webdrv.set_window_size(1280, 640)
    webdrv.get(url)

    html = webdrv.page_source
    soup = BeautifulSoup(html, 'html.parser')
    max_page = 1
    for link in soup.find_all('a'):
        _url = link.get('href')
        if _url is None:
            continue
        m_url = _url
        if not like_url(_url):
            if not _url.startswith('/'):
                _url = site_url + '/' + _url 
            else:
                _url = site_url + _url
        if 'http://www.baloo.co/movies/page/' in _url:
            path_s = _url.split('/')
            page = int(path_s[len(path_s) - 1])
            if page > max_page:
                max_page = page
        else:
            print('++: {}'.format(_url))

    print('max_page: {}'.format(max_page))
    for pg in range(1,max_page+1):
        _url = 'http://www.baloo.co/movies/page/{}'.format(pg)
        print('===> {}'.format(_url))
        webdrv.get(_url)

        html = webdrv.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            _url = link.get('href')
            if _url is None:
                continue
            m_url = _url
            if not like_url(_url):
                if not _url.startswith('/'):
                    _url = site_url + '/' + _url 
                else:
                    _url = site_url + _url
            if 'http://www.baloo.co/movie/' in _url:
                print('MV: {}'.format(_url))
            else:
                print('++: {}'.format(_url))

    with open('list.html', 'w', encoding='utf-8') as fp:
        try:
            _pretty = BeautifulSoup(html, 'lxml').prettify()
            fp.write(str(_pretty))
            fp.close()
        except:
            pass


def get_tv_list(webdrv, url):
    webdrv.set_window_size(1280, 640)
    webdrv.get(url)

    html = webdrv.page_source
    soup = BeautifulSoup(html, 'html.parser')
    max_page = 1
    for link in soup.find_all('a'):
        _url = link.get('href')
        if _url is None:
            continue
        m_url = _url
        if not like_url(_url):
            if not _url.startswith('/'):
                _url = site_url + '/' + _url 
            else:
                _url = site_url + _url
        if 'http://www.baloo.co/tvseries/page/' in _url:
            path_s = _url.split('/')
            page = int(path_s[len(path_s) - 1])
            if page > max_page:
                max_page = page
        else:
            print('++: {}'.format(_url))

    print('max_page: {}'.format(max_page))
    for pg in range(1,max_page+1):
        _url = 'http://www.baloo.co/tvseries/page/{}'.format(pg)
        print('===> {}'.format(_url))
        webdrv.get(_url)

        html = webdrv.page_source
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            _url = link.get('href')
            if _url is None:
                continue
            m_url = _url
            if not like_url(_url):
                if not _url.startswith('/'):
                    _url = site_url + '/' + _url 
                else:
                    _url = site_url + _url
            if 'http://www.baloo.co/tvserie/' in _url:
                print('TV: {}'.format(_url))
            else:
                print('++: {}'.format(_url))


def exit_web(webdrv):
    webdrv.quit()


if __name__=='__main__':
    webdrv = init_webdriver()
    #get_mv_list(webdrv, seek_urls[0])
    get_tv_list(webdrv, seek_urls[1])
    exit_web(webdrv)
    sys.exit()
