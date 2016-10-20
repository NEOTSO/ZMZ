# -*- coding: utf-8 -*-

import urllib
import urllib2
import cookielib
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ZMZ:
	def __init__(self):
		self.headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
		self.auth_url = 'http://www.zimuzu.tv/User/Login/ajaxLogin'	# 登录url
		self.get_url = 'http://www.zimuzu.tv/gresource/list/32532'	# 下载的url

		self.data={
			"account":"", # 输入用户名
			"password":"" # 输入密码
		}
		self.opener = None
		self.links = {'category': '', 'name': '', 'link': []}


	def login(self):
		cookieJar = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
		post_data = urllib.urlencode(self.data)
		request = urllib2.Request(self.auth_url, post_data, self.headers)
		response = self.opener.open(request)


	def start(self):
		print 'start...'
		self.login()
		result = self.opener.open(self.get_url)
		content = result.read().decode('utf-8')
		pattern_name = re.compile('<span class="tv">(.*?)</span>(.*?)<span', re.S)
		name = re.findall(pattern_name, content)
		self.links['category'] = name[0][0]
		self.links['name'] = name[0][1]
		pattern_links = re.compile('<div class="media-box">(.*?)<div class="media-control">', re.S)
		links = re.findall(pattern_links, content)
		pattern_formats = re.compile('<div class="media-list".*?<h2 class="it">(.*?)</h2>.*?<ul>(.*?)</ul>', re.S)
		formats = re.findall(pattern_formats, links[0])
		for format in formats:
			pattern_episodes = re.compile('<li class="clearfix".*?class="f7 lk">(.*?)</a>.*?<font class="f3">(.*?)</font>.*?<div class="fr">(.*?)</div>', re.S)
			pattern_ed2k = re.compile('<a href="ed2k(.*?)" type="ed2k', re.S)
			pattern_magnet = re.compile('<a href="magnet(.*?)" type="magnet', re.S)
			pattern_thunder = re.compile('thunderhref="(.*?)">', re.S)
			episodes = re.findall(pattern_episodes, format[1])
			sn = {'format': '', 'episode': []}
			sn['format'] = format[0]
			for episode in episodes:
				e = {'name': '', 'size': '', 'source': {}}
				e['name'] = episode[0]
				e['size'] = episode[1]
				s = {'ed2k': '', 'magnet': '', 'thunder': ''}
				ed2k = re.findall(pattern_ed2k, episode[2])
				if ed2k:
					s['ed2k'] = 'ed2k' + ed2k[0]
				else:
					s['ed2k'] = ''
				magnet = re.findall(pattern_magnet, episode[2])
				if magnet:
					s['magnet'] = 'magnet' + magnet[0]
				else:
					s['magnet'] = ''
				thunder = re.findall(pattern_thunder, episode[2])
				if thunder:
					s['thunder'] = thunder[0]
				else:
					s['thunder'] = ''
				e['source'] = s
				sn['episode'].append(e)
			self.links['link'].append(sn)


		self.getlinks()
		print 'end..'

	def getlinks(self):
		links = self.links
		with open('magnet.txt', 'a') as f:
			f.write('########' + links['category'] + '\t' + links['name'] + '\n\n\n')
			for link in links['link']:
				f.write(link['format'] + '\n')
				episodes = link['episode']
				for episode in episodes:
					f.write(episode['name'] + '\t' + episode['size'] + '\n')
					source = episode['source']
					f.write('####ed2k####\n' + source['ed2k'] + '\n')
					f.write('###magnet###\n' + source['magnet'] + '\n')
					f.write('###thunder###\n' + source['thunder'] + '\n')
					f.write('\n')
				f.write('\n\n')
			
		print 'Mission Completed'

zmz = ZMZ()
zmz.start()