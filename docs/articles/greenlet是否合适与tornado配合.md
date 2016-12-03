Title: greenlet是否合适与tornado结合？
Date: 2016-10-07 09:12
Author: jmpews
Category: tornado
Tags: tornado
Slug: tornado-with-greenlet

之前在tornado上实现一个线程和Future的结合(`tornado中ioloop-yield-Future与thread的配合.md`). 之后有个想法就是将greenlet和tornado结合, 今天抽时间具体看了下.

greenlet本质是模拟线程调度, 但线程的调度是由OS系统控制的. 

先说线程,比如sleep操作，超过时间片自动切换到另一个线程(时间片调度算法)。

再说greenlet, 在greenlet中需要程序员自己去做调度, 切换堆栈上下文等。然而关键就在于**何时进行协程切换?**,这需要自己去判断, 比如gevent库，在进行socket的monkey_pach时, 会进行几个操作. 1. 把socket改为因为非阻塞 2. 建立一个后台事件循环机制, 在connect时, 将当前协程切换(switch)到主协程继续执行, 并注册事件响应回调函数为'切换到该协程', 这样就完成了协程间的切换, 这里事件循环机制的存在也正是为了**解决何时切换到被挂起的协程以继续执行**而存在.

**gevent和go的实现不一样**

那yield和greenlet在实现上有区别么, yield是根据`PyFrameObject`和字节码, 通过保存`PyFrameObject`和恢复来实现. 相当于封装了一层C的API, 而greenlet就是按照函数切换机制，在C和汇编的层面完成. 可以看下这篇[Greenlet切换源码分析].

那greenlet是否更合适与Torando配合? 如果要配合怎么配合?

首先我不觉得greenlet很适合与tornado配合, 因为本质还是需要用tornado的ioloop和future, 作为协程切换的关键. 

如果确实需要使用，关键就是, 将Future的`set_result`的回调函数改为greenlet的协程就可以了.
