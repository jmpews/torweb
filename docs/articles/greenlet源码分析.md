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

## 怎么自建greenlet协程?

借助系统调用相关函数, 形成调用栈, 保存父调用, 以便在函数执行完毕后返回.

## 怎么进行greenlet协程切换?

先进行C层的栈切换, 将当前函数的栈保存到堆中, 之后进行Python层的栈(`PyFrameObject`)切换

## 关于调用栈的基本概念

#### C层栈

* 栈是从高地址向低地址
* 汇编用栈来传递过程参数, 存储返回信息, 保存寄存器用于以后恢复. 函数调用分配的那部分称为栈帧, 栈帧其实是两个指针寄存器, `%ebp` 为帧指针(栈底,高地址), 而 `%esp` 为栈指针(栈顶, 低地址). 一般来说以 `%ebp` 作为基址进行参数等相关寻址, 因为 `%esp` 为变址.
* `%eip` 指向当前执行

#### Python层栈

> Python虚拟机有一个栈帧的调用栈，其中栈帧的是 `PyFrameObject`，位于 `Include/frameobject.h`, 栈帧保存了给出代码的的信息和上下文，其中包含最后执行的指令，全局和局部命名空间，异常状态等信息。`f_valueblock` 保存了数据， `b_blockstack` 保存了异常和循环控制方法。每一个栈帧都拥有自己的数据栈和block栈，独立的数据栈和block栈使得解释器可以中断和恢复栈帧。

 ---
> Python代码首先被编译为字节码，再由Python虚拟机来执行。一般来说，一条Python语句对应着多条字节码（由于每条字节码对应着一条C语句，而不是一个机器指令，所以不能按照字节码的数量来判断代码性能）。

---
> 许多个 `PyFrameObject` 通过 `f_back` 连成一串链表，表示了帧与帧之间的先后、调用顺序。Python中帧在运行时需要额外的内存，比如a = b + c这段代码，那么需要先请读入b、c，再算a，除此之外还有局部变量等需要保存在栈中，因此最后有一个 `f_localsplus` 指向这块多出来的内存，大小则在编译时计算出来保存在 `f_stacksize中`，这块内存具体用来依次保存 `locals`(局部变量), `cellvars`, `freevars`(后两个和闭包的实现有关), 动态栈(`f_valuestack` 指向栈底, `f_stacktop` 则维持栈顶）。

---
> `yield` 协程(`object/genobject.c`)实现: `PyGen_New(PyFrameObject *f)
` -> `gen_iternext(PyGenObject *gen)` -> `gen_send_ex(PyGenObject *gen, PyObject *arg, int exc)` -> `PyEval_EvalFrameEx `, 整个过程的两个核心函数 `gen_send_ex` 和 `PyEval_EvalFrameEx `, `gen_send_ex` 用于设置生成器的状态和返回栈(`f->f_back = tstate->frame(当前线程状态的执行栈)`), 以及对于执行结果的判断和异常处理, `PyEval_EvalFrameEx` 则是执行字节码, 当遇到 `YIELD_VALUE` 则利用 `goto` 跳出 `for(;;)` 至 `fast_yield` 返回结果(返回前使用(`f->f_stacktop = stack_pointer`) 保存了栈顶指针, 默认来说对于一个Frame栈来说, 在其执行完后 `f->f_stacktop` 应该为 `NULL`, 但是对于 `yield` 当以后再次调用 `PyEval_EvalFrameEx`, 会根据之前保存的 `f->f_stacktop` 恢复 `stack_pointer`, 所以需要保存 `f->f_stacktop`)

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

#### @Python中进行栈切换



**Python的栈和C栈不同, Python栈建立在虚拟机上**, 关于具体原理请参考 《Python源码剖析》

总体上说, 就是先进行C栈切换, 对于 `%eip` 设置(即执行位置的切换, 如何switch到另一个协程执行, 如何在协程执行完毕后返回父协程继续执行)需要设置 `top_frame`.

关于Python中的 `PyFrameObject` 在 `Include/frameobject.h`定义, 

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
    /* 保存状态(%EIP), 进行Python层的frame状态保存 */
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
    /* 恢复状态(%EIP), 进行Python层的frame状态恢复 */
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

## greenlet的相关QA?

#### @应该开启多少greenlet协程?

应该根据具体的带宽和机器配置

#### @greenlet协程数受什么限制?

因为greenlet是用户自控制的微线程, 保存greenlet栈状态是将栈状态保存在堆中, 所以是受内存大小的限制. 但是即使开启了很多的线程去并发, 但由于带宽不足, 扫描速度依然不会快.

---

##参考资料：

http://www.cnblogs.com/coder2012/p/4990834.html

http://simple-is-better.com/news/677

http://cyrusin.github.io/2016/07/28/greenlet-20150728/

http://rootk.com/post/Python-greenlet.html

http://114.215.135.238:8001/?p=108

http://www.cnblogs.com/alan-babyblog/p/5353152.html

http://devrel.qiniucdn.com/data/20110704093648/index.html
