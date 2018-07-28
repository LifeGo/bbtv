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

site_url = 'http://www.baloo.co/'
site_path = 'www/'

visited_links = []
error_links = []
run_log = []

FTYPE_TEXT = 0
FTYPE_DATA = 1
FTYPE_JPEG = 2
FTYPE_PAGE = 3
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
	if href is None:
		return False

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

	if '/page/' in href:
		return(FTYPE_PAGE)	##PAGE => INDEX

	if 'baloo.co/admin/covers/' in href:
		return(FTYPE_DATA)	##JPG => DATA

	for ft in ftext:
		if href.lower().endswith(ft):
			return(FTYPE_TEXT)	##TEXT

	for ft in fdata:
		if href.lower().endswith(ft):
			return(FTYPE_DATA)	##DATA

	return(FTYPE_INDEX)  ##INDEX


def save_res(bs, element, check):
	links = bs.find_all(element)

	for l in links:
		if element == 'link':
			_url = l.get('href')
		elif element == 'script':
			_url = l.get('src')
		elif element == 'img':
			_url = l.get('src')

		if _url is None:
			continue

		if check in _url or element == 'img':
			if not like_url(_url):
				if _url.startswith('/'):
					_url = 'http://www.baloo.co' + _url
				else:
					_url = 'http://www.baloo.co/' + _url

			if not 'baloo.co' in _url:
				continue

			if _url in visited_links:
				continue

			Fstream = False
			ftype = chk_href_type(_url)
			if FTYPE_DATA == ftype:
				Fstream = True

			fname = _url.replace(site_url, '').strip()
			if 'http://baloo.co/admin/covers/' in fname:
				fname = _url.replace('http://baloo.co/', '').strip()

			log_pr('::{}: {} => {}'.format(ftype, _url, fname))
			try:
				r = requests.get(_url, stream=Fstream)
			except requests.exceptions.ConnectionError:
				error_links.append(_url)
				continue

			if r.status_code != 200:
				error_links.append(_url)
				continue

			visited_links.append(_url)
			os.makedirs(os.path.dirname(site_path + fname), exist_ok=True)
			with open(site_path + fname, 'wb') as f:
				if FTYPE_DATA == ftype:
					f.write(r.raw.read())
				else:
					f.write(r.text.encode('utf-8'))
				f.close()
			log_save('.tmp.log')


log_idx = 0

def crawl(link, depth):
	global log_idx
	log_pr('>>>: @{}'.format(depth))
	if not like_url(link) or chk_skip(link) or not chk_baloo(link):
		log_pr('---: {}'.format(link))
		return()

	if link in visited_links or link.lower().endswith('/'):
		log_pr('---: {}'.format(link))
		return()

	ftype = chk_href_type(link)
	## if FTYPE_INDEX != ftype:
	##	   log_pr('---: {}'.format(link))
	##	   return()

	if FTYPE_INDEX == ftype:
		flink = link + '/index.html'
		mlink = link
	elif FTYPE_PAGE == ftype:
		flink = link
		path_s = link.split('/')
		mlink = 'http://'
		for i in range(2, len(path_s)-1):
			mlink += path_s[i] + '/'
		log_pr('**-: {}'.format(mlink))
	else:
		log_pr('---: {}'.format(link))
		return()

	log_pr('+++: {}'.format(link))
	visited_links.append(link)

	try:
		r = requests.get(link)
	except requests.exceptions.ConnectionError:
		log_pr('Connection Error - {}'.format(link))
		return()

	if r.status_code != 200:
		log_pr('Invalid Response - {}'.format(r.status_code))
		return()

	fname = flink.replace(site_url, '').strip()
	if 'http://baloo.co/admin/covers/' in fname:
		fname = flink.replace('http://baloo.co/', '').strip()

	log_pr('::{}: {} => {}'.format(ftype, link, fname))
	os.makedirs(os.path.dirname(site_path + fname), exist_ok=True)
	with open(site_path + fname, 'wb') as f:
		text = r.text
		#text = text.replace('href="/"','href="#"')
		#text = text.replace('href="/','href="')
		#text = text.replace('src="/','src="')
		f.write(text.encode('utf-8'))
		f.close()

	bs = BeautifulSoup(r.text, 'html.parser')
	save_res(bs=bs, element='link', check='.css')
	save_res(bs=bs, element='script', check='.js')
	save_res(bs=bs, element='img', check='.n.o')

	for link in bs.find_all('a'):
		_url = link.get('href')

		if chk_skip(_url) or '-' in _url:
			log_pr('---: {}'.format(_url))
			continue

		m_url = _url
		if not like_url(_url):
			if _url.startswith('/'):
				_url = 'http://www.baloo.co' + _url
			else:
				_url = 'http://www.baloo.co/' + _url

		log_idx += 1
		if log_idx > 10:
			log_idx = 0
		log_save('.{}.log'.format(log_idx))
		if chk_baloo(_url) and not _url in visited_links and not _url in error_links and mlink in _url:
			try:
				log_pr('>->: {} >-> {}'.format(mlink, _url))
				crawl(_url, depth+1)
			except:
				error_links.append(_url)

	log_pr('<-<: {} <-< {}'.format(mlink, _url))
	log_pr('<<<: @{}'.format(depth))

def run():
	crawl('http://www.baloo.co', 0)
	return()

	log_pr('Link crawled\n')
	for link in visited_links:
		log_pr('--- {}'.format(link))

	log_pr('\n\nLink error\n')
	for link in error_links:
		log_pr('--- {}'.format(link))

if __name__=='__main__':
	run()
	log_save('run.log')
