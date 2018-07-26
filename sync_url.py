#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# standard imports
import os
import sys
import time
import re
import json

import requests
from bs4 import BeautifulSoup

base_dir = ''
site_url = 'http://www.baloo.co/'
site_path = 'www/'

visited_links = []
error_links = []
run_log = []

FTYPE_TEXT = 0
FTYPE_DATA = 1
FTYPE_JPEG = 1
FTYPE_INDEX= 4


def wait_second(sec):
    print('wait for {} second ...'.format(sec))
    time.sleep(sec)


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


def like_url(href):
    if href.strip().startswith('http') and '.' in href:
       return True

    return False


def chk_skip(href):
    if href is None:
        return True

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


def chk_href_type(href):
    ftext = [
        '.js',
        '.jsp',
        '.css',
        '.xml',
        '.htm',
        '.html',
        '.log',
        '.txt',
        '.cpp',
    ]
    fdata = [
        '.png',
        '.jpg',
        '.gif',
        '.apk',
        '.zip',
        '.gz',
        '.bz2',
        '.bin',
        '.dat',
    ]

    if 'baloo.co/admin/covers/' in href:
        return(FTYPE_DATA)  ##JPG => DATA

    for ft in ftext:
        if href.lower().endswith(ft):
            return(FTYPE_TEXT)  ##TEXT

    for ft in fdata:
        if href.lower().endswith(ft):
            return(FTYPE_DATA)  ##DATA

    return(FTYPE_INDEX)  ##INDEX


def save_res(link):
    if not 'baloo.co' in link:
        return()

    flink = link
    ftype = chk_href_type(link)
    if FTYPE_INDEX == ftype:
        flink = link + '/index.html'

    fstream = False
    if FTYPE_DATA == ftype:
        fstream = True

    try:
        r = requests.get(link, stream=fstream)
    except requests.exceptions.ConnectionError:
        print('Connection Error - {}'.format(link))
        return()

    if r.status_code != 200:
        print('Invalid Response - {}'.format(r.status_code))
        return()

    fname = flink.replace(site_url, '').strip() 
    if 'http://baloo.co/admin/covers/' in fname:
        fname = flink.replace('http://baloo.co/', '').strip() 

    fname = flink.replace(site_url, '').strip() 
    log_pr('::{}: {} => {}'.format(ftype, link, fname))
    os.makedirs(os.path.dirname(site_path + fname), exist_ok=True)
    with open(site_path + fname, 'wb') as f:
        if FTYPE_INDEX == ftype:     ## INDEX => TEXT
            #f.write(r.text.encode('utf-8'))
            text = r.text.replace('href="/"','href="#"')
            text = text.replace('href="/','href="')
            text = text.replace('src="/','src="')
            f.write(text.encode('utf-8'))
        elif FTYPE_TEXT == ftype:    ## TEXT
            f.write(r.text.encode('utf-8'))
        elif FTYPE_DATA == ftype:    ## DATA
            f.write(r.raw.read())
        f.close()


def crawl(link):
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

        if link.lower().endswith('/'):
            print('0. Working with : {} >>> SKIP'.format(link))
            return()

        if not 'baloo.co' in link:
            return()

        try:
            r = requests.get(link)
        except requests.exceptions.ConnectionError:
            print('Connection Error - {}'.format(link))
            return()

        if r.status_code != 200:
            print('Invalid Response - {}'.format(r.status_code))
            return()

        flink = link
        ftype = chk_href_type(link)
        if FTYPE_INDEX == ftype:
            flink = link + '/index.html'

        fname = flink.replace(site_url, '').strip() 
        if 'http://baloo.co/admin/covers/' in fname:
            fname = flink.replace('http://baloo.co/', '').strip() 

        os.makedirs(os.path.dirname(site_path + fname), exist_ok=True)
        with open(site_path + fname, 'wb') as f:
            #f.write(r.text.encode('utf-8'))
            text = r.text.replace('href="/"','href="#"')
            text = text.replace('href="/','href="')
            text = text.replace('src="/','src="')
            f.write(text.encode('utf-8'))
            f.close()

        soup = BeautifulSoup(r.text, 'html.parser')
        for link in soup.find_all('img'):
            _url = link.get('src')

            if chk_skip(_url) or '-' in _url:
                log_pr('---: {}'.format(_url))
                continue

            m_url = _url
            if not like_url(_url):
                if _url.startswith('/'):
                    _url = 'http://www.baloo.co' + _url 
                else:
                    _url = 'http://www.baloo.co/' + _url 

            save_res(_url)

        for link in soup.find_all('a'):
            _url = link.get('href')

            if chk_skip(_url) or '-' in _url:
                log_pr('---: {}'.format(_url))
                continue

            m_url = _url
            if not like_url(_url):
                if _url.startswith('/'):
                    _url = 'http://www.baloo.co' + _url 
                    #_url = site_url + '/' + _url 
                else:
                    _url = 'http://www.baloo.co/' + _url 
                    #_url = site_url + _url
            #print('HREF: {} => {}'.format(m_url, _url))

            log_save('run_tmp.log')

            if chk_baloo(_url):
                crawl(_url)


def run():
    crawl('http://www.baloo.co')
    return()

    print('Link crawled\n')
    for link in visited_links:
        print('--- {}'.format(link))
    
    print('\n\nLink error\n')
    for link in error_links:
        print('--- {}'.format(link))

if __name__=='__main__':
    run()
    log_save('run.log')
    #sys.exit()
