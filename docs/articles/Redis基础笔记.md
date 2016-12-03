Title: Redis基础笔记
Date: 2015-09-19 03:43
Author: jmpews
Category: redis
Tags: python,redis
Slug: redis-python

## 1.Pipelines
> Pipelines are a subclass of the base Redis class that provide support for buffering multiple commands to the server in a single request.

```
pipe=r.pipeline()
pipe.set('a',1)
pipe.set('b',2)
pipe.get('a')
pipe.get('b')
pipe.execute()
#[True, True, b'1', b'2']
```

## 2.事务

**Important:事务中每个命令的执行结果都是最后一起返回的，无法讲前一条命令的结果作为下一条命令的参数。**

事务实现`incr()`，不能在事务中实现+1的操作。`watch`监视一个变量直到`execute()`,如果在此期间变量值被修改则异常。

```
with r.pipeline() as pipe:
    while 1:
        try:
            # put a WATCH on the key that holds our sequence value
            pipe.watch('OUR-SEQUENCE-KEY')
            # after WATCHing, the pipeline is put into immediate execution
            # mode until we tell it to start buffering commands again.
            # this allows us to get the current value of our sequence
            current_value = pipe.get('OUR-SEQUENCE-KEY')
            next_value = int(current_value) + 1
            # now we can put the pipeline back into buffered mode with MULTI
            pipe.multi()
            pipe.set('OUR-SEQUENCE-KEY', next_value)
            # and finally, execute the pipeline (the set command)
            pipe.execute()
            # if a WatchError wasn't raised during execution, everything
            # we just did happened atomically.
            break
       except WatchError:
            # another client must have changed 'OUR-SEQUENCE-KEY' between
            # the time we started WATCHing it and the pipeline's execution.
            # our best bet is to just retry.
            continue
```

transaction,更简便的实现方式

> A convenience method named “transaction” exists for handling all the boilerplate of handling and retrying watch errors. It takes a callable that should expect a single parameter, a pipeline object, and any number of keys to be WATCHed. Our client-side INCR command above can be written like this, which is much easier to read:

`transaction(func,'key')`，该函数参数为可调函数`func(pipe)`(自动传入一个pipe参数)和需要监视的key

```
def client_side_incr(pipe):
    current_value = pipe.get('OUR-SEQUENCE-KEY')
    next_value = int(current_value) + 1
    pipe.multi()
    pipe.set('OUR-SEQUENCE-KEY', next_value)

r.transaction(client_side_incr, 'OUR-SEQUENCE-KEY')
#[True]
```

## 3.发布订阅

基本code

```
import redis
db=redis.StrictRedis(host='linevery.com', port=6379, db=0)
p = db.pubsub()
# 忽略订阅消息
p = r.pubsub(ignore_subscribe_messages=True)
# 订阅channel
p.subscribe('channel1', 'channel2')
# 通配符订阅
p.psubscribe('channel*')
# 发送消息，返回有几个channel接收到message
r.publish('channel1', 'some data')
# 获取消息 {'channel': 'my-first-channel', 'data': 'some data', 'pattern': None, 'type': 'message'}
p.get_message()
# 退订channel
p.unsubscribe()
p.punsubscribe('my-*')
```

`get_message()`的回调函数

```
def my_handler(message):
	print('MY HANDLER: ', message['data'])
p.subscribe(**{'my-channel': my_handler})
# 直接调用回调函数，不再返回值。
p.get_message()
```

`get_message()`的几种方式

```
# 循环读取
while True:
    message = p.get_message()
    if message:
        # do something with the message
    time.sleep(0.001)  # be nice to the system :)

# 阻塞读取
for message in p.listen():
    # do something with the message
```

线程loop,必须要存在回调函数的channel，因为thread不能自动的处理message。

```
# 必须存在回调
p.subscribe(**{'my-channel': my_handler})
thread = p.run_in_thread(sleep_time=0.001)
# the event loop is now running in the background processing messages
# when it's time to shut it down...
thread.stop()
```

##
 记住`close()`
