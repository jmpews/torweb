Title: 如何用C为Python写扩展
Date: 2015-08-01 01:00
Author: jmpews
Category: python
Tags: python
Slug: write-extensions-for-python
Summary: 简单介绍, 使用C为python写扩展的简单流程

#### 头文件
`#include "Python.h"`

#### 定义你的函数
* `PyArg_ParseTuple`, 将 `Pyobject* ` 转化为c语言对象

```
static PyObject *
spam_system(PyObject *self,PyObject *args)
{
    const char *command;
    int sts;
    if(!PyArg_ParseTuple(args,"s",&command))
        return NULL;
    sts=system(command);
    if(sts<0)
    {
        PyErr_SetString(SpamError,"System command failed");   
        return NULL;
    }
    return PyLong_FromLong(sts);
}
```

#### 编写方法表(method table)
* `METH_VARARGS`: Python-level parameters to be passed in as a tuple acceptable for parsing via **PyArg_ParseTuple()**
* `METH_VARARGS`: 应该传入Python对象, 然后使用`PyArg_ParseTuple()`转化为C语言使用数据

```
static PyMethodDef SpamMethods[]={
    {"system",spam_system,METH_VARARGS,"Execute a shell command."},
    {NULL,NULL,0,NULL}
};
```

#### 定义就模块结构体

```
static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam", /* name of module */
    NULL,
    -1,
    SpamMethods
};
```

#### 初始化模块
如果有自己定义的异常应该同样初始化


```
PyMODINIT_FUNC
PyInit_spam(void)
{
    PyObject *m;
    m = PyModule_Create(&spammodule);
    if(m==NULL)
        return NULL;
    SpamError = PyErr_NewException("spam.error",NULL,NULL);
    Py_INCREF(SpamError);
    PyModule_AddObject(m,"error",SpamError);
    return m;
}
```

#### 安装模块
需要安装setuptools

```
from distutils.core import setup,Extension

moduleone=Extension('spam',sources=['spammodule.c'])

setup(name='spam',
    version='1.0',
    description='This is spam',
    ext_modules=[moduleone]
)
```

#### 完整代码
`spammodule.c`

```
#include "Python.h"

static PyObject *SpamError;

static PyObject *
spam_system(PyObject *self,PyObject *args)
{
    const char *command;
    int sts;
    if(!PyArg_ParseTuple(args,"s",&command))
        return NULL;
    sts=system(command);
    if(sts<0)
    {
        PyErr_SetString(SpamError,"System command failed");   
        return NULL;
    }
    return PyLong_FromLong(sts);
}


static PyMethodDef SpamMethods[]={
    {"system",spam_system,METH_VARARGS,"Execute a shell command."},
    {NULL,NULL,0,NULL}
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "spam",
    NULL,
    -1,
    SpamMethods
};

PyMODINIT_FUNC
PyInit_spam(void)
{
    PyObject *m;
    m = PyModule_Create(&spammodule);
    if(m==NULL)
        return NULL;
    SpamError = PyErr_NewException("spam.error",NULL,NULL);
    Py_INCREF(SpamError);
    PyModule_AddObject(m,"error",SpamError);
    return m;
}
```
`setup.py`

```
from distutils.core import setup,Extension

moduleone=Extension('spam',sources=['spammodule.c'])

setup(name='spam',
    version='1.0',
    description='This is spam',
    ext_modules=[moduleone]
)
```
