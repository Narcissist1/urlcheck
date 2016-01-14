#!/usr/bin/env python
# -*- coding=utf8 -*-
# author-Zack

import logging
import threading
import urllib2
import Queue
from datetime import datetime as dt
from urlparse import urlparse, urljoin
from bs4 import BeautifulSoup
import time
import re


TARGET_HOST = "http://m.sohu.com/"  # 目标url
WORKQUEUE = Queue.Queue()  			# 待处理队列
VISITED = {}  						# 已检测url集合
THREADNUM = 100  					# 线程数
queueLock = threading.Lock()		# 锁


# 设置log文件
def get_logger(rooturl):
    url = urlparse(rooturl).hostname
    logfilename = "LOGfor-%s_in_%s-%s-%s" % (url,
                                             dt.now().year, dt.now().month, dt.now().day)
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


def urlvalidator(url):
        # Django validator
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return regex.match(url)


# 页节点(边界)判定函数
def stop_flag(url):
    # 当前url hostname
    hostname = urlparse(url).hostname
    if hostname.startswith('m.sohu.com'):
        return True
    if hostname.startswith('m.') and hostname.endswith('sohu.com'):
        # m.tv.sohu.com/m.mail.sohu.com ...
        return True
    return False


# 广搜函数
def bfs_path(url, logger):
    sonlinks = []
    headers = {"User-Agent": 'Mozilla 5.0'}
    req = urllib2.Request(url.encode('utf-8'), headers=headers)
    try:
        response = urllib2.urlopen(req)
        the_page = response.read().decode('utf-8')
        # logger.info('page:%s' % the_page)
        soup = BeautifulSoup(the_page, 'html.parser')
        for link in soup.find_all('a', href=True):
            templink = urljoin(TARGET_HOST, link['href'])
            # logger.info('URl:%s' % templink)
            if templink not in VISITED and urlvalidator(templink) and stop_flag(templink):
                sonlinks.append(templink)
    except urllib2.HTTPError as e:
        # HTTPError 需要在前面
        logger.error('HTTPError:' + str(e.code) + '-' + url)
    except urllib2.URLError as e:
        logger.error('URLError:' + str(e.reason) + '-' +url)
    finally:
        return sonlinks


# 线程类
class myThread(threading.Thread):

    def __init__(self, threadID, queue, task, logger):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.queue = queue
        self.task = task
        self.logger = logger

    def run(self):
        print 'Thread-%d is Working...' % self.threadID
        while len(VISITED) < 1000:
        	print 'Queue size %s' % self.queue.qsize()
        	print 'VISITED size %s' % len(VISITED)
	        if not self.queue.empty():
	            url = self.queue.get()
	            queueLock.acquire()
	            if url not in VISITED:
	                VISITED[url] = 1
	                queueLock.release()
	            else:
	            	queueLock.release()
	                self.queue.task_done()
	                continue
	            sonlinks = self.task(url, self.logger)
	            for link in sonlinks:
	                self.queue.put(link)
	            self.queue.task_done()
	        else:
			    time.sleep(5)


def main():
    logger = get_logger(TARGET_HOST)
    WORKQUEUE.put(TARGET_HOST)
    threads = []
    for i in xrange(THREADNUM):
        t = myThread(i + 1, WORKQUEUE, bfs_path, logger)
        t.daemon = True
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    # 阻塞直到所有任务完成
    # WORKQUEUE.join()
    print 'Job is done'
    print "checked %d urls" % len(VISITED)
    logger.info("checked %d urls" % len(VISITED))

if __name__ == '__main__':
    main()
