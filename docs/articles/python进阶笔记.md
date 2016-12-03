Title: Python进阶笔记
Date: 2015-08-01 00:01
Author: jmpews
Category: python
Tags: python
Slug: python-note
Summary: 总结了python在事件过程中，遇到的进阶知识点。

### 1. class是type的instance
类也是对象
代码解释，解释器会在类创建末尾添加下面一句话啊。type创建一个type实例(即:calss className)，type也存在`__new__`(实例化type)，`__int__`(初始化类)。

`class = type(className, superClasses, attributeDict)`

### 2. `__new__()`实例化
* object是所有类的基类`
* 依次向上调用`__new__实例化类，若父没有定义，则继续直至object基类
* 不能调用自身的`__new__`来实例化对象。`cls.__new__(cls, *args, **kwargs)`这样不可行

```
# cls当前正在实例化的类
def __new__(cls, *args, **kwargs):
    ...  
```

### 3. super继承
对于单继承，当父类修改名字可以避免多次修改

```
class Base(object):
    def __init__(self):
        print "Base created"

class ChildA(Base):
    def __init__(self):
        Base.__init__(self)

class ChildB(Base):
    def __init__(self):
        # Python3 可以直接使用super().__init__()
        super(ChildB, self).__init__()

ChildA() 
ChildB()
```
对于多继承,采用mro顺序调用，相同父类只调用一次

```
class D(A,B,C):
    def __init__(self):
        super(D，self).__init__()
```
### 4. dict的遍历方式

#### 1.采用for遍历dict
不可以在遍历的过程中进行修改

```
dict={1:'a',2:'b',3:'c'}

def add_handler():
    dict[4]='d'
		
for k,v in dict.items():
    if k==3:
        add_handler()
    print(k,v)
```
结果

```
Traceback (most recent call last):
1 a
  File "/Users/jmpews/PycharmProjects/asyncnet/test.py", line 15, in <module>
    for k,v in dict.items():
2 b
RuntimeError: dictionary changed size during iteration
3 c

Process finished with exit code 1
```
#### 2.采用popitem遍历
可以在遍历过程中对dict进行修改，但是遍历后，dict为空

```
dict={1:'a',2:'b',3:'c'}

def add_handler():
    dict[4]='d'

while dict:
    k,v=dict.popitem()
    if k==3:
        add_handler()
    print(k,v)

print(dict)
```
结果

```
1 a
2 b
3 c
4 d
{}
```
### 5. 装饰器高级特性
用装饰器我们可以很好的做一些预处理，但仍然有一些小问题需要我们处理，比如装饰器修饰后函数的`__name__`和`__doc__`属性，我们可以手动`return functools.update_wrapper(_wrapper,func)`，也可以采用`@functools.wraps(_wrapper)`。

```
def hello(func):
    def _wrapper(*args,**kwargs):
        import inspect
        # 将参数转化为字典类型
        func_args=inspect.getcallargs(func,*args,**kwargs)
        if func_args:
            for k,v in func_args.items():
                print('key=',k,'value=',v)
        print('hello call ',func.__name__)
        return func(*args,**kwargs)
    import functools
    # 更新装饰器的__name__等属性
    return functools.update_wrapper(_wrapper,func)

@hello
def function(name):
    print('my name is',name)

function('Amy')

print(function.__name__)
```
结果

```
key= name value= Amy
hello call  function
my name is Amy
function

```
### 6. classmethod与工厂方法
工厂方法把选择具体实现的功能延迟到子类去实现。

```
class Pizza(object):
	def __init__(self,ing):
		self.ing=ing;
	@classmethod
	def from_fridge(cls,fridge):
		return cls(fridge.get_a()+fridge.get_b())
		
class A_Pizza(Pizza):
	pass
	
A_Pizza.from_fridge(fridge)
```

### 7. 简单工厂模式和抽象工厂模式
[抽象工厂模式](http://www.cnblogs.com/jerryxing/archive/2013/01/23/2873408.html)

### 8. with的使用
```
class LockContext(object):
    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        self.Lock()

    def __exit__(self, type, value, traceback):
        if type != None:
            pass
        self.Unlock()
        return False
```

也可以使用`contextmanager`，使用yield返回值

```
@contextmanager
    def locked(lock):
        lock.acquire()
        try:
            yield values
        finally:
            lock.release()
```

### 11. `locals()`返回局部变量字典，包含所有键值对

### 12. `time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())`

### 13. python进制相关
'\x2d' 主要是用来表是一个不能直接显示的单字节字符的编码 

'0x2d' 应该算是一个标准的16进制表示的字符串，可以通过int('0x2d', 16) 转换为int 类型的值

```
65=ord('A')
```

### 14.生成器
```
def mygenerator():
    yield 1

gen=mygenerator()
import inspect
inspect.getgeneratorstate(gen)
```
### 15.参数传入
```
def foo(*args, **kwargs):
    print "Positional arguments are:"
    print args
    print "Keyword arguments are:"
    print kwargs

#可以看出args为元组，**kwargs为字典    
>>> foo(1, 2, 3)
Positional arguments are:
(1, 2, 3)
Keyword arguments are:
{}
>>> foo(1, 2, name='Adrian', framework='Django')
Positional arguments are:
(1, 2)
Keyword arguments are:
{'framework': 'Django', 'name': 'Adrian'}
```

### 16. 系统路径
```
glob 查找路径
```
### 17. 对**理解,表示列表参数

```
a,*b,c=[1,2,3,4]
# 巧妙的递归
items=[1,2,3,4,5,6,7,8]
def sum(items):
    head,*rest=items
    return head+sum(rest) if rest else head

```
