Title: greenlet源码分析
Date: 2015-12-27 03:43
Author: jmpews
Category: greenlet
Tags: 协程,coroutine,greenlet
Slug: read-greenlet

> 2016-12-10 更新

协程可以说是让程序员自己做控制的微线程.

## 为什么使用greenlet?

可以同时开启多个微线程(准确说应该是依次开启, 当遇到需要 I/O 的地方, 自动切换到另一个协程), 从而可以实现超大并发.

## greenlet的相关QA?

#### @应该开启多少greenlet协程?

应该根据具体的带宽和机器配置

#### @greenlet协程数受什么限制?

因为greenlet是用户自控制的微线程, 保存greenlet栈状态是将栈状态保存在堆中, 所以是受内存大小的限制. 但是即使开启了很多的线程去并发, 但由于带宽不足, 扫描速度依然不会快.

## 怎么自建greenlet协程?

借助系统调用相关函数, 形成调用栈, 保存父调用, 以便在函数执行完毕后返回.

## 怎么进行greenlet协程切换?

先进行C层的栈切换, 将当前函数的栈保存到堆中, 之后进行python层的栈切换, 设置 `top_frame`.

## 关于调用栈的基本概念

#### 栈

* 栈是从高地址向低地址
* 汇编用栈来传递过程参数, 存储返回信息, 保存寄存器用于以后恢复. 函数调用分配的那部分称为栈帧, 栈帧其实是两个指针寄存器, `%ebp` 为帧指针(栈底,高地址), 而 `%esp` 为栈指针(栈顶, 低地址). 一般来说以 `%ebp` 作为基址进行参数等相关寻址, 因为 `%esp` 为变址.

## 协程的切换

#### @特例:C语言中的函数调用(栈切换)

其实协程的一个很特殊的例子，就是函数调用。下面这个例子在 `main` 中调用 `func`

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

用gcc生成汇编代码(建议在redhat或centos下`

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
栈的切换发生在函数调用, 从 `main` 函数进入 `func`.

```
1. 首先将需要传入func的参数入栈。
2. push <func 的下一条指令>
3. 进入func
4. push bp (保存栈底)
5. mov sp,bp (设置新栈顶)

---至此为止的栈，属于上一个栈

6. 开始为局部变量分配地址
8. 执行func
7. leave = mov bp,sp,pop bp (恢复 main 函数栈)
8. ret (返回 func 的下一条指令继续执行)
```

---

#### @python中进行栈切换



**python的栈和C栈不同, python栈建立在虚拟机上**, 关于具体原理请参考 《python源码剖析》

总体上说, 就是先进行C栈切换, 对于 `%eip` 设置(即执行位置的切换, 如何switch到另一个协程执行, 如何在协程执行完毕后返回父协程继续执行)需要设置 `top_frame`.

greenlet 的结构

```
typedef struct _greenlet {
  PyObject_HEAD
  char* stack_start;
  char* stack_stop;
  char* stack_copy;
  intptr_t stack_saved;
  struct _greenlet* stack_prev;
  struct _greenlet* parent;
  PyObject* run_info;
  struct _frame* top_frame;
  int recursion_depth;
  PyObject* weakreflist;
  PyObject* exc_type;
  PyObject* exc_value;
  PyObject* exc_traceback;
  PyObject* dict;
} PyGreenlet;
```

下面分析 greenlet 的具体调用过程

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

首先: `gr1.switch("func1")` 会调用 `g_switch` 函数, 其中 `target=gr1,args=('func1')`

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

`gr1(new_greenlet)`, 默认 `stack_start = NULL(没有运行)` ,`stack_stop = NULL(没有启动)`, 因而执行`g_initialstub()`

dummymarker设置为栈底

##### 为什么要将dummymarker栈底设置于此处？

`g_initialstub`的栈中包含函数需要的参数等数据，然而`&dummymarker`的位置恰为`g_initialstub`栈的ebp。

#### `g_initialstub` 分析

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

设置当前greenlet的 `stack_prev` 为 `ts_current`, 即上一个正在运行的栈

`PyEval_CallObjectWithKeywords` 过程中可能会切换另一个greenlet, 否则函数运行到结束

#### `g_switchstack` 分析
```
static int g_switchstack(void)
{
  int err;
  {
    /* save state */
    /* 保存状态(%EIP), 进行python层的frame状态保存 */
    PyGreenlet* current = ts_current;
    PyThreadState* tstate = PyThreadState_GET();
    current->recursion_depth = tstate->recursion_depth;
    current->top_frame = tstate->frame;
    current->exc_type = tstate->exc_type;
    current->exc_value = tstate->exc_value;
    current->exc_traceback = tstate->exc_traceback;
  }
  /* 汇编实现C层栈切换, 分不同平台 */
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
    /* 恢复状态(%EIP), 进行python层的frame状态恢复 */
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

#### `slp_switch`

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

        /* 重要! current在此暂停，target从此处继续之前的状态之前 */
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

---

##参考资料：

http://rootk.com/post/python-greenlet.html

http://114.215.135.238:8001/?p=108

http://www.cnblogs.com/alan-babyblog/p/5353152.html
