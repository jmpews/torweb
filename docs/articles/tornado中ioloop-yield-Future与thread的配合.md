Title: tornado中ioloop-yield-Future与thread的配合
Date: 2016-10-07 09:12
Author: jmpews
Category: tornado
Tags: tornado
Slug: ioloop-yield-future-thread

在写项目[torweb](https://github.com/jmpews/torweb), 需要有一个分离一个线程去完成耗时操作.

把tornado的Future、Python里的Yield和线程结合起来，处理阻塞函数。可以查看[tests/test_thread_future.py](https://github.com/jmpews/torweb/blob/master/tests/test_thread_future.py) ，具体分析可以查看 http://jmpews.github.io/posts/tornado-future-ioloop-yield.html

```
from threading import Thread
class ThreadWorker(Thread):
    '''
    线程Future
    '''
    def __init__(self, future, func, *args, **kwargs):
        Thread.__init__(self)
        self.future =future
        self.func =func
        self.args = args
        self.kwargs = kwargs
        print('worker init...')

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.future.set_result(result)

def run_with_thread_future(*args, **kwargs):
    '''
    如何利用yield, future和线程的配合
    http://jmpews.github.io/posts/tornado-future-ioloop-yield.html
    :param args:
    :param kwargs:
    :return:
    '''
    def wraps_func(func):
        @functools.wraps(func)
        def wraps_args(*args, **kwargs):
            future = Future()
            work = ThreadWorker(future, func, *args, **kwargs)
            work.start()
            return future
        return wraps_args
    return wraps_func
```

