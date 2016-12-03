Title: Torando的IOLoop和Applicaion过程分析
Date: 2015-10-10 00:01
Author: jmpews
Category: tornado
Tags: tornado
Slug: tornado-read
Summary: 阅读tornado源码来学习加深对服务器端的理解

## Application和IOLoop初始化

![初始化](../images/tornado初始化流程.jpg)


`IOLoop.current()`返回当前的loop，若无，则进行单例初始化。

`IOLoop.instance()`进行单例初始化

`IOLoop()`进行初始化

`Configurable.__new__()` 父类初始化

`IOLoop.configure_default()`根据不同平台实现子类
