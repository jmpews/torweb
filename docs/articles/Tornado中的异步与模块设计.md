Title: Tornado中的异步与模块设计(yield&yield from)
Date: 2016-2-27 03:43
Author: jmpews
Category: tornado
Tags: tornado
Slug: tornado-yield-module-design

## Tornado异步实质
使用Tornado的yield进行异步`reponse=yield Async.fetch('http://example.com')`,在这个过程，用一句话说就是注册IO可读事件的handler(回调函数)到IOLoop(事件循环机制)。其中yield本质是回调，相当于回调`send(result)`，那么最后也就是`response=result`.

举一个Tornado典型的异步例子

```
class AsyncHandler(RequestHandler):
    @asynchronous
    @coroutine
    def post(self, *args, **kwargs):
      httpclient=AsyncHTTPClient()
      resp=yield httpclient.fetch('http://www.abc.com')
      self.write(resp.body)
```
## 如何进行tornado异步的模块化设计
现在遇到的情况就是，假如进行模块化设计。比如：写个util模块函数，函数内进行异步调用(重复使用,并且不能直接展开到post函数内,减少耦合)

```
def get_info(username):
    do something...
    httpclient = AsyncHTTPClient()
    # 仅为生成器
    resp1 = yield httpclient.fetch('http://www.abc.com')
    resp2 = yield httpclient.fetch('http://www.abc.com')

    do something...

    return resp1 + resp2

class WebHandler(RequestHandler):
    @asynchronous
    @coroutine
    def post(self, *args, **kwargs):
        other func()...
        # 错误!!!，后面仅仅是个生成器，需要的是Future才能和coroutine配合
        result=yield get_info(username)
        other func()...
        return result_final
```
## 装饰器实现解决

```
@wrap_yield
def get_info(username):
    do something...
    httpclient = AsyncHTTPClient()
    #仅为生成器
    resp1 = yield httpclient.fetch('http://www.abc.com')
    resp2 = yield httpclient.fetch('http://www.abc.com')

    do something...

    return resp1 + resp2

def wrap_yield(func):
    @functools.wraps
    def wrapper(*args, **kwargs):
        _g = func(*args, **kwargs)

		# return future
		_f = _g.send(None)
		while True:
			try:
				# return future
				_s =  yield(_f)
				_f = _g.send(_s)
			except StopIteration:
				break
			excpet Exception as e:
				try:
					_f = _g.send(e)
				except StopIteration:
					break

class WebHandler(RequestHandler):
    @asynchronous
    @coroutine
    def post(self, *args, **kwargs):

        other func()...

        resp = yield get_info(username)
        return result_final
```

## `yield from` Trick (PEP-380)

```
# http://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-new-yield-from-syntax-in-python-3
# 关于yield from的例子
def reader():
    """A generator that fakes a read from a file, socket, etc."""
    for i in range(4):
        yield '<< %s' % i

# 不使用yield from
def reader_wrapper(g):
    # Manually iterate over data produced by reader
    for v in g:
        yield v
wrap = reader_wrapper(reader())
for i in wrap:
    print(i)

# 使用yield from
def reader_wrapper(g):
    yield from g

# Result
<< 0
<< 1
<< 2
<< 3
```

可以看官方对于`yield from`给出的等价py实现

```
# https://www.python.org/dev/peps/pep-0380/
Python 3 syntax is used in this section.

1. The statement

::

    RESULT = yield from EXPR

is semantically equivalent to

::

    _i = iter(EXPR)
    try:
        _y = next(_i)
    except StopIteration as _e:
        _r = _e.value
    else:
        while 1:
            try:
                _s = yield _y
            except GeneratorExit as _e:
                try:
                    _m = _i.close
                except AttributeError:
                    pass
                else:
                    _m()
                raise _e
            except BaseException as _e:
                _x = sys.exc_info()
                try:
                    _m = _i.throw
                except AttributeError:
                    raise _e
                else:
                    try:
                        _y = _m(*_x)
                    except StopIteration as _e:
                        _r = _e.value
                        break
            else:
                try:
                    if _s is None:
                        _y = next(_i)
                    else:
                        _y = _i.send(_s)
                except StopIteration as _e:
                    _r = _e.value
                    break
    RESULT = _r
```

具体如何解决tornado中异步模块设计问题

```
def get_info(username):
    do something...
    httpclient = AsyncHTTPClient()
    #仅为生成器
    resp1 = yield httpclient.fetch('http://www.abc.com')
    resp2 = yield httpclient.fetch('http://www.abc.com')

    do something...

    return resp1 + resp2


class WebHandler(RequestHandler):
    @asynchronous
    @coroutine
    def post(self, *args, **kwargs):

        other func()...

        resp = yield from get_info(username)
        return result_final
```

## 参考链接:

---

https://www.python.org/dev/peps/pep-0380/

http://stackoverflow.com/questions/9708902/in-practice-what-are-the-main-uses-for-the-new-yield-from-syntax-in-python-3
