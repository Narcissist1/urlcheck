#!/usr/bin/env python
# -*- coding=utf8 -*-

import threading
import os
import Queue
from datetime import datetime as dt
from urlparse import urlparse
from bs4 import BeautifulSoup

TARGET_URL = "http://m.sohu.com/"


class Main_check(object):

	def __init__(self, rooturl):
		super(Main_check, self).__init__()
		self.rooturl =rooturl
		self.logger = self.get_logger()
		self.queue=Queue.Queue()
		self.queue.put(self.rooturl)
		self.visited={}

	# 设置log文件
	def get_logger(self):
		url = urlparse(self.rooturl).hostname
		logfilename="LOGfor-%s_in_%s-%s-%s" % (url,dt.now().year,dt.now().month,dt.now().day)
		logfilename+='.log'
		logger = logging.getLogger(logfilename)
		logger.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		fh = logging.FileHandler(logfilename)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger


	# 广搜函数
	def bfs_path(self, url):
		user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
		headers = { 'User-Agent' : user_agent }
		req = urllib2.Request(url.encode('utf-8'),headers)
		try:
			response = urllib2.urlopen(req)
			the_page = response.read().decode('utf-8')
			soup = BeautifulSoup(page,'html.parser')
			for link in soup.find_all('a'):
			    print(link.get('href'))
		except urllib2.HTTPError as e:
			# HTTPError 需要在前面
			self.logger.error('HTTPError:'+str(e.code)+'\n'+str(e.read())+url)
		except urllib2.URLError as e:
			self.logger.error('URLError:'+str(e.reason)+url)
		finally:
			pass
		



	# 页节点(边界)判定函数
	def stop_flag(url):
		# 当前url hostname
		hostname = urlparse(url).hostname
		if hostname == 'm.sohu.com':
			return True
		if hostname.startswith('m.') and hostname.endswith('sohu.com'):
			# m.tv.sohu.com ...
			return True
		return False



		
# class Check_thread(threading.Thread):
# 	"""docstring for Check_thread"""
# 	def __init__(self, arg):
# 		super(Check_thread, self).__init__()
# 		self.arg = arg


if __name__ == '__main__':
	mc= Main_check(TARGET_URL)
