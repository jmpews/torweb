# jmp

## Features(even Tricks?)

### utils
#### how to get args?
1. `get_cleaned_post_data_http_error` `get_cleaned_query_data_http_error` 获取参数，如果获取不到返回`HTTPError(400)`
2. `get_cleaned_query_data` `get_cleaned_post_data` 获取参数，返回自定义异常

## Tricks
### cache with trick

在`/app/cache.py` 缓存一些需要**面向所有用户使用**的缓存，比如缓存文章分类、热门文章分类、系统状态

```
system_status_cache = [0, 0, 0, 0]

def update_system_status_cache():
    '''
    系统状态cache
    :return:
    '''
    from threading import Thread

    class MonitorWorker(Thread):
        '''
        监视系统状态线程
        '''
        def __init__(self, name, systatus):
            Thread.__init__(self)
            self.name = name
            self.systatus = systatus
        def run(self):
            logger.debug("start monitor system status...")
            import psutil, datetime, time
            while True:
                try:
                    time.sleep(30)
                    s1 = psutil.cpu_percent()
                    s2 = psutil.virtual_memory()[2]
                    try:
                        s3 = len(psutil.net_connections())
                    except:
                        s3 = 'unkown'
                    s4 = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d")
                    self.systatus[0] = s1
                    self.systatus[1] = s2
                    self.systatus[2] = s3
                    self.systatus[3] = s4
                except KeyboardInterrupt:
                    break

    monitor = MonitorWorker('system', system_status_cache)
    monitor.start()
    
update_system_status_cache()
```

### deal with exception 

```
def exception_deal(exceptions):
    '''
    捕获get, post函数异常
    :param exceptions:
    :return:
    '''
    def wrapper_func(func):
        # 保存原函数信息
        @functools.wraps(func)
        def wrapper_args(handler, *args, **kwargs):
            try:
                func(handler, *args, **kwargs)
            except Exception as ex:
                if isinstance(ex, PageNotFoundError):
                    handler.redirect(ex.redirect_url)
                elif isinstance(ex, RequestMissArgumentError):
                    handler.write(ex.msg)
                # for e in exceptions:
                #     if isinstance(ex, e):
                #         handler.write('oh, catch exp in the args list...\n')
        return wrapper_args
    return wrapper_func
```

### coroutine with (thread+future)
```
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
    如何利用future和线程的配合
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

### function time cost
```
def timeit(func):
    '''
    计算函数执行时间
    :param func:
    :return:
    '''
    def wrapper(*args, **kwargs):
        start = time.clock()
        func(*args, **kwargs)
        end = time.clock()
        end = time.clock()
        # ColorPrint.print('> Profiler: '+func.__qualname__+'used: '+str((end - start) * 1e6) + 'us')
        ColorPrint.print('> Profiler: '+func.__qualname__+'used: '+str((end - start)) + 'us')
    return wrapper
```

