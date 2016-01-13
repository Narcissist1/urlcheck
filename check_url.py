#!/usr/bin/env python
# -*- coding=utf8 -*-
# author-Zack

import threading
import os
import Queue
from datetime import datetime as dt
from urlparse import urlparse
from bs4 import BeautifulSoup
import time

TARGET_URL = "http://m.sohu.com/"
WORKQUEUE = Queue.Queue()
VISITED = {}


# 设置log文件
def get_logger(rooturl):
	url = urlparse(rooturl).hostname
	logfilename = "LOGfor-%s_in_%s-%s-%s" % (url, dt.now().year, dt.now().month, dt.now().day)
	logfilename += '.log'
	logger = logging.getLogger(logfilename)
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter(
	    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh = logging.FileHandler(logfilename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


# 广搜函数
def bfs_path(url):
	sonlinks = []
	user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5)'
	headers = { 'User-Agent' : user_agent }
	req = urllib2.Request(url.encode('utf-8'),headers)
	try:
		response = urllib2.urlopen(req)
		the_page = response.read().decode('utf-8')
		soup = BeautifulSoup(page,'html.parser')
		for link in soup.find_all('a'):
			templink=link.get('href')
			if stop_flag(templink):
			    sonlinks.append(templink)
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


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter


    def run(self):
        print "Starting " + self.name
       # 获得锁，成功获得锁定后返回True
       # 可选的timeout参数不填时将一直阻塞直到获得锁定
       # 否则超时后将返回False
        threadLock.acquire()
        print_time(self.name, self.counter, 3)
        # 释放锁
        threadLock.release()
		


def main():
	logger = getLogger(TARGET_URL)
	WORKQUEUE.put(TARGET_URL)


if __name__ == '__main__':
	main()
	
