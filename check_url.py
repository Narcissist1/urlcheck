#!/usr/bin/env python
# -*- coding=utf8 -*-
# author-Zack

import logging
import threading
import urllib2
import Queue
from datetime import datetime as dt
from urlparse import urlparse
from bs4 import BeautifulSoup
import time

TARGET_URL = "http://m.sohu.com/"  	# 目标url
WORKQUEUE = Queue.Queue()  			# 待处理队列
VISITED = {}  						# url是否处理过
THREADNUM = 5  						# 线程数
URLCOUNTER = 0

# 设置log文件
def get_logger(rooturl):
	url = urlparse(rooturl).hostname
	logfilename = "LOGfor-%s_in_%s-%s-%s" % (url, dt.now().year, dt.now().month, dt.now().day)
	logfilename += '.log'
	logger = logging.getLogger(logfilename)
	logger.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	fh = logging.FileHandler(logfilename)
	fh.setLevel(logging.DEBUG)
	fh.setFormatter(formatter)
	logger.addHandler(fh)
	return logger


# 广搜函数
def bfs_path(url,logger):
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
		logger.error('HTTPError:'+str(e.code)+'\n'+str(e.read())+url)
	except urllib2.URLError as e:
		logger.error('URLError:'+str(e.reason)+url)
	finally:
		return sonlinks


# 页节点(边界)判定函数
def stop_flag(url):
	# 当前url hostname
	hostname = urlparse(url).hostname
	if hostname == 'm.sohu.com':
		return True
	if hostname.startswith('m.') and hostname.endswith('sohu.com'):
		# m.tv.sohu.com/m.mail.sohu.com ...
		return True
	return False


# 线程类
class myThread(threading.Thread):
    def __init__(self, threadID, queue, task, logger):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.queue = queue
        self.task = task
        self.logger = logger

    def run(self):
    	while not self.queue.empty():
    		print 'Thread-%d is Working...' % self.threadID
	    	url = self.queue.get()
	        if url not in VISITED:
	        	VISITED[url]=1
	        	URLCOUNTER += 1
	        	self.queue.task_done()
	        else:
	        	self.queue.task_done()
	        	continue
	        sonlinks = self.task(url,self.logger)
	        for link in sonlinks:
	        	self.queue.put(link)
	        time.sleep(3)


def main():
	logger = get_logger(TARGET_URL)
	WORKQUEUE.put(TARGET_URL)
	threads=[]
	for i in xrange(THREADNUM):
		t = myThread(i+1,WORKQUEUE,bfs_path,logger)
		t.daemon = True
		t.start()
		threads.append(t)

	for thread in threads:
		thread.join()

	# 阻塞直到所有任务完成
	WORKQUEUE.join()
	print 'Job is done'
	print "checked %d urls" % URLCOUNTER

if __name__ == '__main__':
	main()
	
