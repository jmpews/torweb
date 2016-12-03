Title: Flask
Date: 2016-07-14 09:59
Author: jmpews
Category: flask
Tags: flask
Slug: study-flask

**文档地址 `http://docs.jinkan.org/docs/flask/`**

## 基础命令

### 应用上下文
> Flask 背后的设计理念之一就是，代码在执行时会处于两种不同的“状态”（states）。 当 Flask 对象被实例化后在模块层次上应用便开始隐式地处于应用配置状态。一直到第一个请求还是到达这种状态才隐式地结束。当应用处于这个状态的时候 ，你可以认为下面的假设是成立的：

> 程序员可以安全地修改应用对象, 目前还没有处理任何请求, 你必须得有一个指向应用对象的引用来修改它。不会有某个神奇的代理变量指向你刚创建的或者正在修改的应用对象的, 相反，到了第二个状态，在处理请求时，有一些其它的规则:当一个请求激活时，上下文的本地对象（ flask.request 和其它对象等） 指向当前的请求, 你可以在任何时间里使用任何代码与这些对象通信

如何创建应用上下文?

1. 当一个请求上下文被压栈时， 如果有必要的话一个应用上下文会被一起创建。
2. 显式地调用 `app_context()`

应用场景?

> 应用上下文会在必要时被创建和销毁。它不会在线程间移动，并且也不会在不同的请求之间共享。正因为如此，它是一个存储数据库连接信息或是别的东西的最佳位置。内部的栈对象叫做 flask._app_ctx_stack

### 请求上下文
** 文档:http://docs.jinkan.org/docs/flask/reqcontext.html **

如何构造请求上下文进行测试?

```
# 也可以使用 with app.test_request_context('/?next=http://example.com/'):
from flask import request, url_for
app = Flask('test')

# 使用 test_client 测试
with app.test_client() as c:
        resp = c.get('/users/me')
        print resp

# 使用测试上下文        
ctx = app.test_request_context('/?next=http://example.com/')
ctx.push()

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('index')
redirect_url()
```
