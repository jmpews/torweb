Title: Greenlet源码分析
Date: 2015-12-27 03:43
Author: jmpews
Category: greenlet
Tags: 协程,coroutine,greenlet
Slug: read-greenlet

## Summary:

协程可以算是自定义控制切换的微线程。

## 栈切换的本质
#### 1.栈

* 栈是从高地址向低地址
* 栈大小固定不变
* 栈帧(stack frame)，机器用栈来传递过程参数，存储返回信息，保存寄存器用于以后恢复，以及本地存储。为单个过程(函数调用)分配的那部分栈称为栈帧。栈帧其实是两个指针寄存器，寄存器%ebp为帧指针(栈底-高地址)，而寄存器%esp为栈指针(栈顶-低地址)

#### 2.切换

* 切换首先需要切换执行位置(`top_frame`)
* 但是当切换执行位置，同时要切换到目的栈，同时要保证栈内数据没有丢失，且没有被无意修改。这就需要栈数据的保存与恢复(`slp_switch`)。

## 如何进行切换？
### 1. C栈切换

其实协程的一个很特殊的例子，就是函数调用。下面这个例子在main中调用func

```
#include<stdio.h>
int func(int arg)
{
    int d=4;
    int e=5;
    int f;
    f=d+e+arg;
    return f;
}

int main()
{
    int a=1;
    int b=2;
    int c=3;
    func(c);
    c=a+b;
}
```
用gcc生成汇编code，建议在redhat或centos下

```
.file   "stackpointer.c"
.text
.globl func
.type   func, @function
func:
pushl   %ebp
movl    %esp, %ebp
subl    $16, %esp
movl    $4, -12(%ebp)
movl    $5, -8(%ebp)
movl    -8(%ebp), %eax
movl    -12(%ebp), %edx
leal    (%edx,%eax), %eax
addl    8(%ebp), %eax
movl    %eax, -4(%ebp)
movl    -4(%ebp), %eax
leave
ret
.size   func, .-func
.globl main
.type   main, @function
main:
pushl   %ebp
movl    %esp, %ebp
subl    $20, %esp
movl    $1, -12(%ebp)
movl    $2, -8(%ebp)
movl    $3, -4(%ebp)
movl    -4(%ebp), %eax
movl    %eax, (%esp)  
call    func
movl    -8(%ebp), %eax
movl    -12(%ebp), %edx
leal    (%edx,%eax), %eax
movl    %eax, -4(%ebp)
leave
ret
.size   main, .-main
.ident  "GCC: (GNU) 4.4.7 20120313 (Red Hat 4.4.7-11)"
.section        .note.GNU-stack,"",@progbits
```

```
函数调用
从main函数进入func

1. 首先将需要传入func的参数入栈。

2. push『call func』=下一条地址(IP压栈),jmp 『func』的函数地址(设置IP)

4. 进入func

5. `push bp`

6. `mov sp,bp`

---至此为止的栈，属于上一个栈

7. 开始为局部变量分配地址

8. `leave = mov bp,sp,pop bp`

9. `ret`
```

#### `call func`
* `push ip`，保存下一条指令的地址
* `jump func`，修改ip跳转到func执行函数

####  func
* push ebp,保存bp
* mov esp,ebp，设置新的栈底。
* 以新的bp进行偏移，保存临时、本地变量，完成函数功能
* leave(等价与mov ebp，esp；pop ebp)恢复esp和ebp
* ret 恢复ip，回到call的下一条指令继续执行。

### 2. Python栈切换
我们进行的切换方式与此类似，但是python的栈和c栈不同，python栈建立在虚拟机上。

总体上说，就是先进行c栈切换，关于ip设置跳转到下条指令执行(即执行位置的切换,如何跳到函数位置开始执行，如何从函数返回原来位置执行)，需要在python上实现`top_frame`的设置。

具体细节参考:

* [python的Greenlet模块源码分析](http://rootk.com/post/python-greenlet.html)
* [greenlet栈帧切换细节](http://114.215.135.238:8001/?p=108)

## switch具体实现


几个注意点：

* 导入greenlet会初始化一个`main_greenlet`，并设置current为`main_greenlet`
* greenlet运行结束，会返回到父greenlet执行

```
from greenlet import greenlet  

def func1(arg):  
    print (arg)  
    gr2.switch()  
    print ("func1 end")  

def func2():  
    print ("fun2 come")  

#设置parent为main_greenlet
gr1 = greenlet(func1)  
gr2 = greenlet(func2)  
value = gr1.switch("fun1 come")  
print (value)  
```
首先：
```
gr1.switch("func1")
```
会调用`g_switch函数`，其中`target=gr1,args=('func1')`

```
static PyObject *
g_switch(PyGreenlet* target, PyObject* args, PyObject* kwargs)
{
  ...
  while (target) {
  if (PyGreenlet_ACTIVE(target)) {
    ts_target = target;
    err = g_switchstack();
    break;
  }
  if (!PyGreenlet_STARTED(target)) {
    void* dummymarker;
    ts_target = target;
    err = g_initialstub(&dummymarker);
    if (err == 1) {
      continue; /* retry the switch */
    }
    break;
  }
  target = target->parent;
  }
  ...
}
```
* `gr1(new_greenlet)`，默认`stack_start = NULL(没有运行)`,`stack_stop = NULL(没有启动)`，因而执行`g_initialstub()`
* dummymarker设置为栈底
* 为什么要将dummymarker栈底设置于此处？

`g_initialstub`的栈中包含函数需要的参数等数据，然而`&dummymarker`的位置恰为`g_initialstub`栈的ebp。

### `g_initialstub` 分析

代码已简化

```
static int GREENLET_NOINLINE(g_initialstub)(void* mark))
{
  ...
  /* 设置stack_stop，表明start该greenlet */
  self->stack_start = NULL;
  self->stack_stop = (char*) mark;

  /* 设置target的上一个活动栈 */
  /* Example:g1_greenlet.stack_prev=main_greenlet */
  if (ts_current->stack_start == NULL) {
    /* ts_current is dying */
    self->stack_prev = ts_current->stack_prev;
  }
  else {
    self->stack_prev = ts_current;
  }
  /* 核心代码，进行栈切换 */
  err = g_switchstack();

  /* 标志greenlet正在运行，将要运行PyEval_CallObjectWithKeywords */
  self->stack_start = (char*) 1;  /* running

  /* 设置当前运行参数为parent参数 */
  self->run_info = green_statedict(self->parent);
  /* 开始执行函数 */
  /* 注意:可能在该函数运行过程中，存在switch其他的greenlet，否则运行到函数结束 */
  result = PyEval_CallObjectWithKeywords(
    run, args, kwargs);

  /* 标志函数结束 */
  self->stack_start = NULL;  /* dead */

  /* 函数结束切换到parent运行 */
  for (parent = self->parent; parent != NULL; parent = parent->parent) {
    result = g_switch(parent, result, NULL);
}

```
* 设置当前greenlet的`stack_prev`为`ts_current`，即上一个正在运行的栈
* `PyEval_CallObjectWithKeywords`过程中可能会切换另一个greenlet，否则函数运行到结束

### `g_switchstack` 分析
```
static int g_switchstack(void)
{
	int err;
	{   /* save state */
	    /* 保存线程状态或者说EIP */
		PyGreenlet* current = ts_current;
		PyThreadState* tstate = PyThreadState_GET();
		current->recursion_depth = tstate->recursion_depth;
		current->top_frame = tstate->frame;
		current->exc_type = tstate->exc_type;
		current->exc_value = tstate->exc_value;
		current->exc_traceback = tstate->exc_traceback;
	}
	/* 汇编实现栈切换，分不同平台 */
	err = slp_switch();
	if (err < 0) {   /* error */
		PyGreenlet* current = ts_current;
		current->top_frame = NULL;
		current->exc_type = NULL;
		current->exc_value = NULL;
		current->exc_traceback = NULL;

		assert(ts_origin == NULL);
		ts_target = NULL;
	}
	else {
	    /* 恢复线程状态，或者说EIP，即跳转执行位置 */
		PyGreenlet* target = ts_target;
		PyGreenlet* origin = ts_current;
		PyThreadState* tstate = PyThreadState_GET();
		tstate->recursion_depth = target->recursion_depth;
		tstate->frame = target->top_frame;
		target->top_frame = NULL;
		tstate->exc_type = target->exc_type;
		target->exc_type = NULL;
		tstate->exc_value = target->exc_value;
		target->exc_value = NULL;
		tstate->exc_traceback = target->exc_traceback;
		target->exc_traceback = NULL;

		assert(ts_origin == NULL);
		Py_INCREF(target);
		ts_current = target;
		ts_origin = origin;
		ts_target = NULL;
	}
	return err;
}
```
* 保存线程状态，即EIP
* 进行C栈切换，汇编实现
* 恢复目标线程状态，即跳转执行位置

### `slp_switch` (核心代码) 分析
```
static int
slp_switch(void)
{
    /* 下面变量保存在栈(current)中 */
    int err;
    void* rbp;
    void* rbx;
    unsigned int csr;
    unsigned short cw;
    register long *stackref, stsizediff;
    /* 这里save的是current线程的状态，变量保存在栈中 */
    __asm__ volatile ("" : : : REGS_TO_SAVE);
    __asm__ volatile ("fstcw %0" : "=m" (cw));
    __asm__ volatile ("stmxcsr %0" : "=m" (csr));
    __asm__ volatile ("movq %%rbp, %0" : "=m" (rbp));
    __asm__ volatile ("movq %%rbx, %0" : "=m" (rbx));
    __asm__ ("movq %%rsp, %0" : "=g" (stackref));
    {
        /* 保存当前线程的数据，包括上面的那些寄存器等等数据 */
        /* 当为new_greenlet直接返回1，无栈可切换 */
        SLP_SAVE_STATE(stackref, stsizediff);

        /* 重要！current在此暂停，target从此处继续之前的状态之前 */
        __asm__ volatile (
            "addq %0, %%rsp\n"
            "addq %0, %%rbp\n"
            :
            : "r" (stsizediff)
            );
        /* 恢复栈(target)中数据 */
        SLP_RESTORE_STATE();
        __asm__ volatile ("xorq %%rax, %%rax" : "=a" (err));
    }
    /* 恢复寄存器变量，这里恢复的是之前保存在target栈中的变量 */
    /* 恢复了target的esp和ebp，因为变量的保存是以ebp进行偏移寻址中，所以当进行恢复时，进行相同偏移，但是因为ebp为已变为之前的target栈，因而恢复的寄存器也仍为之前的状态。 */
    __asm__ volatile ("movq %0, %%rbx" : : "m" (rbx));
    __asm__ volatile ("movq %0, %%rbp" : : "m" (rbp));
    __asm__ volatile ("ldmxcsr %0" : : "m" (csr));
    __asm__ volatile ("fldcw %0" : : "m" (cw));
    __asm__ volatile ("" : : : REGS_TO_SAVE);
    return err;
}
```

很重要的一点，当从恢复ebp和esp开始，current暂停，target继续之前运行，恢复之前数据，恢复的寄存器也仍为之前保存的状态，因为他们是基于ebp的偏移寻址，寻址方式不变，只受ebp的控制。

参考资料：
---
[python的Greenlet模块源码分析](http://rootk.com/post/python-greenlet.html)

[greenlet栈帧切换细节](http://114.215.135.238:8001/?p=108)
