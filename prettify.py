#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import os.path
from bs4 import BeautifulSoup


_href = []
_link = []
_script = []
_img = []


rep_dict = {
	'href="#':'href="/',
	'href="123movies':'href="/123movies',
	'href="cdn-cgi':'href="/cdn-cgi',
	'href="contact':'href="/contact',
	'href="dmca':'href="/dmca',
	'href="episode':'href="/episode',
	'href="faq':'href="/faq',
	'href="genre':'href="/genre',
	'href="gostream':'href="/gostream',
	'href="movie':'href="/movie',
	'href="movies':'href="/movies',
	'href="request':'href="/request',
	'href="subsmovies':'href="/subsmovies',
	'href="terms':'href="/terms',
	'href="tvserie':'href="/tvserie',
	'href="tvseries':'href="/tvseries',
	'href="watchfree':'href="/watchfree',
	'href="watchfree':'href="/watchfree',
	'href="css':'href="/css',
	'src="admin/':'src="/admin/',
	'src="img/':'src="/img/',
	'src="js/':'src="/js/',
	'src="cnd-cgi/':'src="/cnd-cgi/',
	}


def sss_rep():
	cwdir = os.getcwd()

	for root, dirs, files in os.walk(cwdir):
		for name in files:
			if name.lower().endswith('.html'):
				fullname = root + '/' + name
				#print(fullname)
				fs = open(fullname)
				try:
					text = fs.read()
					bs = BeautifulSoup(text, 'html.parser')

					for link in bs.find_all('a'):
						_url = link.get('href')
						if not _url in _href:
							#print('href={}'.format(_url))
							_href.append(_url)

					for link in bs.find_all('link'):
						_url = link.get('href')
						if not _url in _link:
							#print('href={}'.format(_url))
							_link.append(_url)

					for link in bs.find_all('script'):
						_url = link.get('src')
						if not _url in _script:
							#print('href={}'.format(_url))
							_script.append(_url)

					for link in bs.find_all('img'):
						_url = link.get('src')
						if not _url in _img:
							#print('href={}'.format(_url))
							_img.append(_url)
				finally:
					fs.close()

	for href in _href:
		print('href={}'.format(href))
	for href in _link:
		print('link={}'.format(href))
	for href in _script:
		print('script={}'.format(href))
	for href in _img:
		print('img={}'.format(href))


def sss():
	cwdir = os.getcwd()

	for root, dirs, files in os.walk(cwdir):
		for name in files:
			if name.lower().endswith('.html'):
				fullname = root + '/' + name
				print(fullname)
				fs = open(fullname)
				try:
					text = fs.read()
				finally:
					fs.close()

				#for rep in rep_dict:
				#	text = text.replace(rep, rep_dict[rep])

				#soup = BeautifulSoup(text, 'html.parser').prettify()
				soup = BeautifulSoup(text, 'html.parser')
				for div in soup.find_all("div", {'class':'container m-t-lg text-center'}): 
					div.decompose()

				#os.makedirs(os.path.dirname(fullname), exist_ok=True)
				with open(fullname, 'wb') as f:
					text = str(soup)
					f.write(text.encode('utf-8'))
				f.close()


if __name__=='__main__':
	cwdir = os.getcwd()
	print(cwdir)
	#sss_rep()
	sss()
