Title: Python引用计数理解
Date: 2015-11-29 13:01
Author: jmpews
Category: python
Tags: 引用计数
Slug: reference-count

# Summary
引用计数记录指向对象引用的个数，当变为0，则被释放。总结了引用计数的注意点和如何使用。更新：weakref(弱引用)、用弱引用解决引用环问题

# 简介
> It counts how many different places there are that have a reference to an object.When an object’s reference count becomes zero, the object is deallocated

> 记录指向对象引用的个数，当变为0，则被释放

# 使用引用计数的实质
> The only real reason to use the reference count is to prevent the object from being deallocated as long as our variable is pointing to it

> 使用引用计数的唯一理由就是只要还有变量指向就应当阻止对象被释放

# 引用计数的实现
* PyObject* 是什么?
* 引用计数变量 **ob_refcnt**
* 如何操作ob_refcnt (Py_INCREF and Py_DECREF)

## 0x00. PyObject* 是什么?
> This type is a pointer to an opaque data type representing an **arbitrary Python object**. Since all Python object types are treated **the same way** by the Python language in most situations (e.g., assignments, scope rules, and argument passing), it is only fitting that they should be represented by a single C type. Almost all **Python objects live on the heap**: you never declare an automatic or static variable of type PyObject, only pointer variables of type **PyObject* **can be declared.

> 这种数据类型是可以表示任意Python对象的封装数据类型，因此Python对象类型在大多数情况下以相同方式处理。几乎全部的Python的对象存储在**heap堆(由程序员分配malloc)**，因此不可以声明一个PyObject的类型对象(局部变量值保存在stack)，只能是**PyObject* **

## 0x01. 引用计数变量 `**ob_refcnt**`
```
typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    struct _typeobject *ob_type;
} PyObject;
```

## 0x02. 如何操作`ob_refcnt (Py_INCREF and Py_DECREF)`
```
#define Py_INCREF(op) (                         \
    _Py_INC_REFTOTAL  _Py_REF_DEBUG_COMMA       \
    ((PyObject *)(op))->ob_refcnt++)

#define Py_DECREF(op)                                   \
    do {                                                \
        PyObject *_py_decref_tmp = (PyObject *)(op);    \
        if (_Py_DEC_REFTOTAL  _Py_REF_DEBUG_COMMA       \
        --(_py_decref_tmp)->ob_refcnt != 0)             \
            _Py_CHECK_REFCNT(_py_decref_tmp)            \
        else                                            \
        _Py_Dealloc(_py_decref_tmp);                    \
    } while (0)
```
# 什么时候操作引用计数
**仅有当你需要保护这个变量不被释放时才使用INCREF**

具体：
* 创建一个Object* 对象
* 处理函数返回的对象
* 借用引用(borrow)
* 偷取引用(Steal)

注: 不需要对每个**本地变量(stack变量)**的引用+1，因为当一个变量创建并且有一个指针指向时，默认INC，然而当变量失去作用范围(stack栈)又会DEC，两者抵消。

## 0x00. 创建一个Object* 对象
### Example1: 源码分析
#### 0x0000.针对long类型变量分析
```
PyObject *l, *x;
x = PyLong_FromLong(1L);
```
#### 0x0001. PyLong_FromLong() [longobject.c]
调用_PyLong_New()创建新long对象
```
PyObject *
PyLong_FromLong(long ival)
{
    PyLongObject *v;
    ...
    //something done
        v = _PyLong_New(1);
    ...
    //something done
    return (PyObject *)v;
}
```
#### 0x0002. _PyLong_New() [longobject.c]
调用**PyObject_MALLOC()**分配内存，调用**PyObject_INIT_VAR()**初始化为PyLongOject\*类型，完成PyObject*相关项的初始化，比如类型项等等。

**注：**关于**PyObject_MALLOC()[obmalloc.c]**，采用**内存池**进行内存管理，此处不详细介绍
[Python内存管理](http://blog.csdn.net/dbzhang800/article/details/6685269)

```
PyLongObject *
_PyLong_New(Py_ssize_t size)
{
    PyLongObject *result;
    if (size > (Py_ssize_t)MAX_LONG_DIGITS) {
        PyErr_SetString(PyExc_OverflowError,
                        "too many digits in integer");
        return NULL;
    }
    result = PyObject_MALLOC(offsetof(PyLongObject, ob_digit) +
                             size*sizeof(digit));
    if (!result) {
        PyErr_NoMemory();
        return NULL;
    }
    return (PyLongObject*)PyObject_INIT_VAR(result, &PyLong_Type, size);
}
```
#### 0x0003. PyObject_INIT_VAR() [objimp.h]

```
#define PyObject_INIT(op, typeobj) \
    ( Py_TYPE(op) = (typeobj), _Py_NewReference((PyObject *)(op)), (op) )
#define PyObject_INIT_VAR(op, typeobj, size) \
    ( Py_SIZE(op) = (size), PyObject_INIT((op), (typeobj)) )
```
#### 0x0004. 宏展开(Macro Expansion) Py_TYPE() _Py_NewReference() [object.h]
最终发现调用创建PyObject\*变量时 **初始化op_refcnt为1**

```
#define Py_TYPE(ob)             (((PyObject*)(ob))->ob_type)
#define Py_REFCNT(ob)           (((PyObject*)(ob))->ob_refcnt)
#define _Py_NewReference(op) (                          \
    _Py_INC_TPALLOCS(op) _Py_COUNT_ALLOCS_COMMA         \
    _Py_INC_REFTOTAL  _Py_REF_DEBUG_COMMA               \
    Py_REFCNT(op) = 1)
```

## 0x01. 处理函数返回的对象
很多函数在返回之前会调用Py_INCREF()，因此该函数的caller需要调用Py_DECREF(),以防内存泄露(memory leak)
### Example1: MyCode必须处理pyo，调用Py_DECREF

```
void MyCode(arguments)
{
    PyObject* pyo;
    ...
    pyo = Py_Something(args);
    //Py_DECREF(pyo);
}
```
###  Example2: 如果MyCode传递pyo的所有权，则不能调用Py_DECREF

```
PyObject* MyCode(arguments) {
    PyObject* pyo;
    ...
    pyo = Py_Something(args);
    ...
    return pyo;
}
```
#### 注: 函数返回None则返回之前需要Py_INCREF(Py_None)
[Py_INCREF(Py_None) from stackoverflow](http://stackoverflow.com/questions/15287590/why-should-py-increfpy-none-be-required-before-returning-py-none-in-c)

```
Py_INCREF(Py_None);
return Py_None;
```

## 0x02. 借用引用(borrow)
**仅获得拷贝，引用计数不增加**

产生借用:

* 返回借用引用对象的函数[borrow]
* 传递给函数的对象[borrow]

### 0x000. 返回借用引用对象的函数[borrow]
* PyTuple_GetItem()
* PyList_GetItem()
* PyList_GET_ITEM()
* PyList_SET_ITEM()
* PyDict_GetItem()
* PyDict_GetItemString()
* PyErr_Occurred()
* PyFile_Name()
* PyImport_GetModuleDict()
* PyModule_GetDict()
* PyImport_AddModule()
* PyObject_Init()
* Py_InitModule()
* Py_InitModule3()
* Py_InitModule4()
* PySequence_Fast_GET_ITEM()

#### Example1: PyList_GetItem仅获得对应项目拷贝，不增加引用计数

```
long sum_list(PyObject *list)
{
 int i, n;
 long total = 0;
 PyObject *item;

 n = PyList_Size(list);
 if (n < 0)
     return -1; /* Not a list */
     /* Caller should use PyErr_Occurred() if a -1 is returned. */
 for (i = 0; i < n; i++) {
     /* PyList_GetItem does not INCREF "item".
        "item" is unprotected and borrowed. IMPORTANT!!! */
     item = PyList_GetItem(list, i); /* Can't fail */
     if (PyInt_Check(item))
         total += PyInt_AsLong(item);
 }
 return total;
}
```
#### Example2: PySequence_GetItem获得对象所有权，其返回对象+1，因而每次循环后需要-1.

```
long sum_sequence(PyObject *sequence)
{
 int i, n;
 long total = 0;
 PyObject *item;
 n = PySequence_Length(sequence);
 if (n < 0)
     return -1; /* Has no length. */
     /* Caller should use PyErr_Occurred() if a -1 is returned. */
 for (i = 0; i < n; i++) {
     /* PySequence_GetItem INCREFs item.  IMPORTANT!!!*/
     item = PySequence_GetItem(sequence, i);
     if (item == NULL)
         return -1; /* Not a sequence, or other failure */
     if (PyInt_Check(item))
         total += PyInt_AsLong(item);
     Py_DECREF(item);
 }
 return total;
}
```

### 0x001. 传递给函数的对象[borrow]
> Most functions assume that the arguments passed to them are already protected.Therefore Py_INCREF() is not called inside Function unless Function wants the argument to continue to exist after Caller exits. In the documentation, Function is said to borrow a reference:
> **大多数函数假定传入函数的参数都是受保护的不需要INCREF，除非希望参数在函数exit后仍然存在。官方文档说法是函数借用引用**

> When you pass an object reference into another function, in general, the function borrows the reference from you   if it needs to store it, it will use Py_INCREF() to become an independent owner.
> **你传递对象给一个函数，一般情况来说是函数借用引用，如果你希望保存那么请INCREF，将其变为独立拥有者。**

**PyTuple_SetItem()和PyList_SetItem()**除外，它们**接管传入对象所有权(take over responsibility) or 偷取引用(steal a reference)**
详细见下

## 0x03. 偷取引用(Steal)
**PyTuple_SetItem(tuple,i,item)和PyList_SetItem()接管所有权(take over responsibility) or 偷取引用(steal a reference) item引用**，but not to the tuple or list into which the item is put，即仅仅偷取item引用.

* PyDict_SetItem()非借用，既然是store变量到dict，因此PyDict_SetItem() INCREF它的kye和value
* 但是PyTuple_SetItem()和PyList_SetItem()比较特殊，接管所有权(take over responsibility) or 偷取引用(steal a reference)
* PyTuple_SetItem(tuple,i,item)实现：如果tuple[i]存在PyObject则DECREF，然后tuple[i]设置为item。并且Item并没有INCREF
* PyTuple_SetItem(tuple,i,item)既然是steal，那么**Item之前必须有所有权**
* 如果PyTuple_SetItem()插入item失败，则DECREF item引用计数
* PyTuple_SetItem()是设置Tuple中item的唯一方法

### Example1:
你不需要调用DECREF(x)，PyTuple_SetItem()已经自动调用了,当Tuple被DECREF时，它的item也会被DECREF

```
PyObjetc *t;
PyObject *x;
x=PyIntFromLong(1L);
PyTuple_SetItem(t,0,x);
```
# 总结
* 许多从**其他对象上提取子对象**的函数，通过引用传递所有权，但有一些例外，**PyTuple_GetItem(),PyList_GetItem(),PyDict_GetItem()，和PyDict_GetItemString()**，这些返回的引用是从tuple，list或dict中**借用**的.(借用仅获得拷贝，引用计数并不增加)
* 当你传递一个对象引用给其他函数，这个函数会从借用这个引用，如果需要保存它应该使用Py_INCREF()转换为独立拥有者。但是有例外，**PyTuple_SetItem()和PyList_SetItem()**，直接传递对象所有权
* Python调用一个C函数的返回对象必须拥有引用所有权传递给它的调用者    

# 常见问题
## 0x00. INCREF不可马虎
常见的情况是从list中提取对象，一些操作符可以能会替换或者移除list中某个对象，并且假如这个向对象是用户自定义的calss，包含__del__，然而这个__del__可以执行任意的code，但是这些操作可能会无意的DEC 该list[0]的引用计数，导致free。

```
bug(PyObject *list) {
/*item利用PyList_GetItem借用list引用*/
 PyObject *item = PyList_GetItem(list, 0);
 //修改措施Py_INCREF(item); /* Protect item. */
 /* This function “steals” a reference to item and discards a reference to an item already in the list at the affected position.
 可能引起list中原list[1]中__del__，导致DEClist[0]*/
 PyList_SetItem(list, 1, PyInt_FromLong(0L));
 PyObject_Print(item, stdout, 0); /* BUG! */
 //修改措施:Py_DECREF(item);
}
```
## 0x01. 偷取和借用对比在build list or tuple方面
### Example1: steal a referfence(take over responsibilty)

```
PyObjetc *t;
PyObject *x;
x=PyIntFromLong(1L);
PyTuple_SetItem(t,0,x);
//Dont't Need Py_DECREF()
```
### Example2 borrow a reference

```
/*Better way*/

PyObject *l, *x;
l = PyList_New(3);
x = PyInt_FromLong(1L);
PySequence_SetItem(l, 0, x); Py_DECREF(x);
x = PyInt_FromLong(2L);
PySequence_SetItem(l, 1, x); Py_DECREF(x);
x = PyString_FromString("three");
PySequence_SetItem(l, 2, x); Py_DECREF(x);
```
### 注: 更常见的创建list和tuple的方法
More Common Way to Populate a tuple or list

```
PyObject *t, *l;
t = Py_BuildValue("(iis)", 1, 2, "three");
l = Py_BuildValue("[iis]", 1, 2, "three");
```
# Refer:
[Reference Counting in Python](http://edcjones.tripod.com/refcount.html)

[Extending Python with C or C++](http://www.incoding.org/admin/archives/808.html)

## Two Examples

### Example 1

This is a pretty standard example of C code using the Python API.

```
PyObject*
    MyFunction(void)
    {
        PyObject* temporary_list=NULL;
        PyObject* return_this=NULL;

        temporary_list = PyList_New(1);          /* Note 1 */
        if (temporary_list == NULL)
            return NULL;

        return_this = PyList_New(1);             /* Note 1 */
        if (return_this == NULL)
            Py_DECREF(temporary_list);           /* Note 2 */
            return NULL;
        }

        Py_DECREF(temporary_list);               /* Note 2 */
        return return_this;
    }
```
* Note 1: The object returned by PyList_New has a reference count of 1.
* Note 2: Since temporary_list should disappear when MyFunction exits, it must be DECREFed before any return from the function. If a return can be reached both before or after temporary_list is created, then initialize temporary_list to NULL and use Py_XDECREF().

### Example 2

```
This is the same as Example 1 except PyTuple_GetItem() is used.
    PyObject*
    MyFunction(void)
    {
        PyObject* temporary=NULL;
        PyObject* return_this=NULL;
        PyObject* tup;
        PyObject* num;
        int err;
        tup = PyTuple_New(2);
        if (tup == NULL)
            return NULL;
        err = PyTuple_SetItem(tup, 0, PyInt_FromLong(222L));
        /* Note 1 */
        if (err) {
            Py_DECREF(tup);
            return NULL;
        }
        err = PyTuple_SetItem(tup, 1, PyInt_FromLong(333L));
        /* Note 1 */
        if (err) {
            Py_DECREF(tup);
            return NULL;
        }
        temporary = PyTuple_Getitem(tup, 0);
        /* Note 2 */
        if (temporary == NULL) {
            Py_DECREF(tup);
            return NULL;
        }
        return_this = PyTuple_Getitem(tup, 1);
        /* Note 3 */
        if (return_this == NULL) {
            Py_DECREF(tup);
            /* Note 3 */
            return NULL;
        }
        /* Note 3 */
        Py_DECREF(tup);
        return return_this;
    }
```

* Note 1: If PyTuple_SetItem fails or if the tuple it created is DECREFed to 0, then the object returned by **PyInt_FromLong is DECREFed**.
* Note 2: PyTuple_Getitem does not increment the reference count for the object it returns.
* Note 3: You have no responsibility for DECFREFing temporary.


# 更新
### 1. 弱引用
> 弱引用与强引用相对，指不能确保其引用对象不会被垃圾回收器回收，一个对象若只被弱引用所引用，则被认为是不可访问的。 --wiki

#### 弱引用解决引用环问题
```
# python2.x会出现，python3.x做了改进
class LeakTest(object):
   def __init__(self):
     print 'Object with id %d born here.' % id(self)
   def __del__(self):
     print 'Object with id %d dead here.' % id(self)

def foo():
   A = LeakTest()
   B = LeakTest()
   A.b = B
   B.a = A
if __name__ = ="__main__":
  foo()

RESULT:
Object with id 10462448 born here.
Object with id 10462832 born here.
```
相互引用导致形成环，当对象只有被弱引用时，同样会被回收,因此可做如下修改

```
import weakref
class LeakTest(object):
   def __init__(self):
     print 'Object with id %d born here.' % id(self)
   def __del__(self):
     print 'Object with id %d dead here.' % id(self)

def foo():
   A = LeakTest()
   B = LeakTest()
   A.b = weakref.proxy(B)
   B.a = weakref.proxy(A)
if __name__ = ="__main__":
  foo()
```
#### 弱引用对象使用
弱引用和代理对象都可以设置callback，在没有强引用时，python要进行销毁时调用。

```
>>> from socket import *
>>> import weakref
>>> s=socket(AF_INET,SOCK_STREAM)
>>> ref=weakref.ref(s) # 通过调用弱引用来获取被弱引用的对象
>>> pref=weakref.proxy(s) #代理对象就是弱引用对象
>>> s
<socket.socket fd=8, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 0)>
>>> ref
<weakref at 0x103275598; to 'socket' at 0x10325aee8>
>>> ref()
<socket.socket fd=8, family=AddressFamily.AF_INET, type=SocketKind.SOCK_STREAM, proto=0, laddr=('0.0.0.0', 0)>
>>> pref
<weakproxy at 0x103275548 to socket at 0x10325aee8>
```
