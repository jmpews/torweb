Title: Tornado中的Future,ioloop,yield三者如何完成以'同步协程,异步执行'
Date: 2016-09-05 09:59
Author: jmpews
Category: tornado
Tags: tornado,异步, yield
Slug: tornado-future-ioloop-yield

## Summary:

首先需要明确的，tornado中异步是建立在事件循环机制之上，也就是IOLoop。

Future IOLoop yield 本质仅仅完成了, 协程的切换, 也就是实现了以同步的方式去写异步

本质上非阻塞与异步的实现是在`SimpleAsyncHTTPClient.fetch_impl(simple_httpclient.py) -> self._process_queue(simple_httpclient.py) self._handle_request(simple_httpclient.py) -> self._connection_class(_HTTPConnection)(simple_httpclient.py) -> self.tcp_client.connect()(simple_httpclient.py) -> self._create_stream(tcpclient.py) -> stream.connect(tcpclient.py) -> self._add_io_state(iostream.py)`, 注册事件到ioloop, 等待实现响应触发`self._handle_events(iostream.py)`

## 异步请求例子

```
from tornado.httpclient import AsyncHTTPClient
from tornado import gen
import tornado.ioloop

@gen.coroutine
def fetch_coroutine(url):
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch(url)
    print(response)
fetch_coroutine('http://jmpews.com')
tornado.ioloop.IOLoop.instance().start()
```

伪代码例子

```
def work():
  future = Future()
  ioloop.add_result_callback(future.set_result('result)) // 触发ioloop响应结果时，设置future状态为完成
  return future

def coroutine():
  def wrap_func(func):
    d = func()
    result = next(d) //future
    future.add_done_callback(d.send(result)) // 设置当future状态为完成时，触发send来恢复协程，继续执行func。
    
@coroutine
def func():
  print('step in')
  result = yield work()
  print('step out')
```

## yield : 异步协程同步写法，配合@tornado.gen.coroutine

yield，有两个作用，一个是用于挂起当前函数(yield)，第二个可以相当于封装后的callback(yield send)，只不过它的callback是`generator.send('result')`，用于恢复挂起函数继续执行。这里需要注意的是，我们需要在挂起当前函数时注册事件循环机制的响应callback为`generator.send('result')`。

所以，使用yield的第一个问题就是，在哪里设置的`generator.send('result')`。这里以`AsyncHTTPClient`为例。

## Future : 连接ioloop和yield
提供`set_result`和`set_done`方法，来触发Future上的callback，其中的callback包含`Runner.run()` ，实质为 `generator.send('result')`，也就是在yield中必须要明确的在哪里设置`generator.send('result')`。

## IOLoop : 调度center
注册响应事件的callback为Future的`set_restult()`，等待事件触发

## `AsyncHTTPClient`分析执行流程

```
# 文件信息: tornado.httpclient
# 涉及到类名: AsyncHTTPClient
# 涉及到函数名: fetch

code ignore...

从这段代码得到函数执行流程: 

0-0 .fetch
 ↓
0-1 .fetch_impl(request, handle_response)

回调函数:
handle_response(response)
# 如果设置了callback
future.add_done_callback(handle_future)
```


`handle_response(response)` 设置 future 的 `set_result` 继续查看 `set_result` 的实现
---

```
# 文件信息: tornado.concurrent
# 涉及到类名: Future
# 涉及到函数名: add_done_callback, set_result, _set_done

code ignore...

从这段代码得到函数执行流程: 

set_result(self, result)
 ↓
_set_done(self)
 ↓
for cb in self._callbacks: cb(self)

额外信息执行流程为:

add_done_callback(self, fn)
 ↓
self._callbacks.append(fn)
```

发现 set_result 后, 会调用 `_set_done` 方法，以及各种callback

接下来看下 `tornado.gen.coroutine` 添加了什么 trick 的 callback

---

```
# 文件信息: tornado.gen
# 涉及到函数名: coroutine, _make_coroutine_wrapper

code ignore...

#从这段代码可以得到函数执行流程:

_make_coroutine_wrapper(func, replace_callback=True)
 ↓
result = func(*args, **kwargs)
 ↓
yielded = next(result)
 ↓
Runner(result, future, yielded)
```

上面没有设置什么 callback, 只是启动了这个 generator, 接下来看 Runner, 有没有做什么工作
---

```
# 文件信息: tornado.gen
# 涉及到类名: Runner
# 涉及到函数名: __init__, handle_yield, run

code ignore...

从这段代码可以得到函数执行流程:

__init__(self, gen, result_future, first_yielded)
 ↓
self.handle_yield(first_yielded)
 ↓
self.io_loop.add_future(self.future, lambda f: self.run())
```

最后可以发现在 run 方法中, 设置了 generator 的 send 方法



