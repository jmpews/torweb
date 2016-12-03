Title: 抓取英雄联盟的妹纸信息
Date: 2015-08-29 01:14
Author: jmpews
Category: python
Tags: python,redis,爬虫
Slug: crawler-lol-girls
Summary: 总的来说结合几个站，抓取妹纸ID，并进行相关分析。打算使用Redis做任务队列，然后利用线程池处理。

首先我觉得做爬虫很容易，难点在于如果把爬虫做的有意义，抓取到有价值的信息。两方面，一方面对自己可以数据分析，提炼价值，然而对个人而言好像没卵用，另一方面，可以整合信息，数据二次整理展现，面向用户。

---

### 8.30:
完成了基本的线程池、任务队列、任务产生py、任务消耗py。更新github

[爬取LoL中girls](https://github.com/jmpews/lolgirl)

### 8.31:
在编写程序发现几个注意点。

1. 重视模块化，一个函数仅仅实现一个功能就ok
2. 如果某个地方可能出现异常需要打上标记 TODO等
3. `time.mktime(time.strptime(timestr,'%Y-%m-%d %H:%M:%S'))`字符串转化为时间戳


## redis任务队列的设计
```
__author__ = 'jmpews'
import redis

class RedisQueue(object):
    def __init__(self,name,namespace='queue',**redis_kwargs):
        self.__db=redis.StrictRedis(host='linevery.com', port=6379, db=0)
        self.key = '%s:%s' % (name,namespace)

    def qsize(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.qsize()==0

    def put(self,item):
        self.__db.rpush(self.key,item)
    # 阻塞至超时
    def get(self,block=True,timeout=None):
        if block:
            item=self.__db.blpop(self.key,timeout=timeout)
            item=item[1]
        else:
            item=self.__db.lpop(self.key)

        # item=item[1]
        return item
        
    # 无阻塞的get	 
    def get_notwait(self):
        return self.get(block=False)

```

# threadpool线程池的设计
```
__author__ = 'jmpews'
import threading
from logger import initLogging

# log file
loggg=initLogging('threadpool.log')

# 初始化工作函数和线程数
class ThreadPool(object):
    def __init__(self,func=None,thread_num=5):
        self.threads=[]
        if func==None:
            self.func=None
            print('Error : func is None...')
            return
        self.func=func
        self.__init_threads(thread_num)

    def __init_threads(self,thread_num=5):
        for i in range(thread_num):
            self.threads.append(Worker(self.func))

    def start(self):
        if self.func==None:
            print('func is None...')
            return
        for one in self.threads:
            one.start()

# 线程实例
class Worker(threading.Thread):
    def __init__(self,func=None):
        self.func=func
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                self.func()
            except Exception as e:
                loggg.error(e)
                import traceback
                traceback.print_exc()
            print('======='+self.name+'Done!=======')

# 测试函数
def test():
    def func():
        print('oh,yes!')
    threadpool=ThreadPool(func=func)
    threadpool.start()

#test()
```

## logging日志记录设计
```
__author__ = 'jmpews'
import logging
def initLogging(logFilename='run.log'):
    """Init for logging"""

    # logging.basicConfig(
    #     level = logging.NOTSET,
    #     format = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
    #     datefmt = '%m-%d %H:%M',
    #     filename = logFilename,
    #     filemode = 'w')

    logger=logging.getLogger()
    # 格式
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s')
    # 输出到文件里
    logfile=logging.FileHandler(logFilename)
    logfile.setLevel(logging.NOTSET)
    logfile.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    console.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(logfile)
    return logger
```
