Title: gdb调试笔记
Date: 2016-04-05 03:43
Author: jmpews
Category: gdb
Tags: gdb
Slug: gdb-note

## 命令集锦

#### where/bt
查看当前运行堆栈列表

#### info program
来查看程序的是否在运行，进程号，被暂停的原因。

#### f N
切换到特定栈帧

#### info args
查看当前栈的参数

#### info locals
查看当前栈的局部变量

#### gdb attach pid
挂载特定pid进行调试

#### disassemble function_name
对一段函数进行反汇编

#### x/16xw $eip
dump出来对应地址内容
