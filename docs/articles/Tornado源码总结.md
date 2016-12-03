Title: Tornado源码阅读总结
Date: 2016-2-27 03:43
Author: jmpews
Category: tornado
Tags: tornado
Slug: tornado-summary

## application
1. 基本配置初始化，关键是对路由规则的配置
2. Httpserver的初始化，继承于Configurable，工厂方法设计模式，，基本参数初始化，初始化父类tcpserver(同样也是进行基本参数初始化)
3. Httpserver监听(是指是穿透到tcp进行监听),建立监听socket

## ioloop
事件循环，类似libev，在不同platform实现不同的事件循环机制(epoll,select)

1. IOLoop初始化，继承于Configurable，工厂设计模式

## Tornado值得学习
### Tornado工厂方法
重写`__new__`函数，根据`configurable_base`和`configurable_default`返回子类，然后`initialize(instead of __init__)`进行初始化。IOLoop的初始化过程 `IOLoop() -> Configurable.__new__() -> KQueueIOLoop.initialize() -> PollIOLoop.initialize() -> IOLoop.initialize()`，同时初始化Waker()，用于在timeout之前返回，通过发送一个字符x唤醒

```
class Configurable(object):
    __impl_class = None
    __impl_kwargs = None

    def __new__(cls, *args, **kwargs):
        base = cls.configurable_base()
        init_kwargs = {}
        if cls is base:
            impl = cls.configured_class()
            if base.__impl_kwargs:
                init_kwargs.update(base.__impl_kwargs)
        else:
            impl = cls
        init_kwargs.update(kwargs)
        instance = super(Configurable, cls).__new__(impl)
        # initialize vs __init__ chosen for compatibility with AsyncHTTPClient
        # singleton magic.  If we get rid of that we can switch to __init__
        # here too.
        instance.initialize(*args, **init_kwargs)
        return instance

    @classmethod
    def configurable_base(cls):
        """Returns the base class of a configurable hierarchy.

        This will normally return the class in which it is defined.
        (which is *not* necessarily the same as the cls classmethod parameter).
        """
        raise NotImplementedError()

    @classmethod
    def configurable_default(cls):
        """Returns the implementation class to be used if none is configured."""
        raise NotImplementedError()

    def initialize(self):
        """Initialize a `Configurable` subclass instance.

        Configurable classes should use `initialize` instead of ``__init__``.

        .. versionchanged:: 4.2
           Now accepts positional arguments in addition to keyword arguments.
        """

    @classmethod
    def configure(cls, impl, **kwargs):
        """Sets the class to use when the base class is instantiated.

        Keyword arguments will be saved and added to the arguments passed
        to the constructor.  This can be used to set global defaults for
        some parameters.
        """
        base = cls.configurable_base()
        if isinstance(impl, (unicode_type, bytes)):
            impl = import_object(impl)
        if impl is not None and not issubclass(impl, cls):
            raise ValueError("Invalid subclass of %s" % cls)
        base.__impl_class = impl
        base.__impl_kwargs = kwargs

    @classmethod
    def configured_class(cls):
        """Returns the currently configured class."""
        base = cls.configurable_base()
        if cls.__impl_class is None:
            base.__impl_class = cls.configurable_default()
        return base.__impl_class

    @classmethod
    def _save_configuration(cls):
        base = cls.configurable_base()
        return (base.__impl_class, base.__impl_kwargs)

    @classmethod
    def _restore_configuration(cls, saved):
        base = cls.configurable_base()
        base.__impl_class = saved[0]
        base.__impl_kwargs = saved[1]
```
