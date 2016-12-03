Title: 为Python添加DES_CFB_64加密解密模块
Date: 2016-06-02 09:12
Author: jmpews
Category: python
Tags: python
Slug: python-des-cfb-64

看过一个搞二进制的哥们把99宿舍的搞定了加密解密方式。用的是`des_cfb64`加密的方式，但是用了几个python加密库都不对，就尝试自己给python写了一个模块，用的是openssl的lib

## 核心的加密解密模块

```
#pycet.c
#include "Python.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <openssl/des.h>

char * Encrypt( char *Key, char *Msg, int size);
char * Decrypt( char *Key, char *Msg, int size);
static PyObject *SpamError;

static PyObject *
cet_des_cfb64(PyObject *self,PyObject *args)
{
    unsigned char * txt;
    unsigned int length;
    unsigned char * key;
    unsigned int C;
    char * r;
    int i=0;
    PyObject *result;

    //接受python参数
    if(!PyArg_ParseTuple(args,"s#sI",&txt,&length,&key,&C))
    {
        return NULL;
    }

    //分配result_buffer
    r = malloc(length);

    //加密和解密
    if(C)
        memcpy(r, Encrypt(key, txt, length), length);
    else
        memcpy(r, Decrypt(key, txt, length), length);


    //保存成python结果
    result = PyBytes_FromStringAndSize(r,length);

    //释放malloc
    free(r);
    return result;
}

// 安装约定部分
//
static PyMethodDef SpamMethods[]={
    {"cetdes",cet_des_cfb64,METH_VARARGS,"cet_des_cfb64"},
    {NULL,NULL,0,NULL}
};

static struct PyModuleDef spammodule = {
    PyModuleDef_HEAD_INIT,
    "cetdes",
    NULL,
    -1,
    SpamMethods
};
PyMODINIT_FUNC
PyInit_cetdes(void)
{
    PyObject *m;
    m = PyModule_Create(&spammodule);
    if(m==NULL)
        return NULL;
    SpamError = PyErr_NewException("cetdes.error",NULL,NULL);
    Py_INCREF(SpamError);
    PyModule_AddObject(m,"error",SpamError);
    return m;
}

//des_cfb64_encrypt
char *
Encrypt( char *Key, char *Msg, int size)
{

	static char*    Res;
	int             n=0;
	DES_cblock      Key2;
	DES_key_schedule schedule;

	Res = ( char * ) malloc( size );

	/* Prepare the key for use with DES_cfb64_encrypt */
	memcpy( Key2, Key,8);
	DES_set_odd_parity( &Key2 );
	DES_set_key_checked( &Key2, &schedule );

	/* Encryption occurs here */
	DES_cfb64_encrypt( ( unsigned char * ) Msg, ( unsigned char * ) Res,
			   size, &schedule, &Key2, &n, DES_ENCRYPT );

	 return (Res);
}

//des_cfb64_decrypt
char *
Decrypt( char *Key, char *Msg, int size)
{

	static char*    Res;
	int             n=0;

	DES_cblock      Key2;
	DES_key_schedule schedule;

	Res = ( char * ) malloc( size );

	/* Prepare the key for use with DES_cfb64_encrypt */
	memcpy( Key2, Key,8);
	DES_set_odd_parity( &Key2 );
	DES_set_key_checked( &Key2, &schedule );

	/* Decryption occurs here */
	DES_cfb64_encrypt( ( unsigned char * ) Msg, ( unsigned char * ) Res,
			   size, &schedule, &Key2, &n, DES_DECRYPT );

	return (Res);

}
```

## 安装模块
```
#setup.py
from distutils.core import setup,Extension
moduleone=Extension('cetdes',
        sources=['pycet.c'],
        include_dirs=['/usr/local/opt/openssl/include'],
        library_dirs=['/usr/local/opt/openssl/lib'],
        libraries = ['crypto']
        )
setup(name='cetdes',
    version='1.0',
    description='This is cetdes',
    ext_modules=[moduleone]
)
```

链接`-lcrypto`库,LIB: `-L/usr/local/opt/openssl/lib`,INCLUDE: `-I/usr/local/opt/openssl/include`

#### 参考链接
[Extending Python with C or C++(官方)] https://docs.python.org/3.5/extending/extending.html
