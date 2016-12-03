Title: go基础笔记
Date: 2016-07-08 09:59
Author: jmpews
Category: go
Tags: go
Slug: study-go

## Function
```
//命名的返回值(初始化为相应类型的零值)
func getX2(i int) (x2 int, x3 int) {
    x2 = 2 * i
    x3 = 3 * i
    return
}

//defer(命名返回值)
func test(s string) (n int, err error) {
    defer func() {
        log.Printf("func (%q) = %d, %v", s, n, error)
    }()
    return 7, io.EOF
}

//defer ret = 2(defer 在return后执行)
func f() (ret int) {
    defer func() {
        ret++
    }()
    return 1
}

//传递函数参数
func Add(a, b int) {
    fmt.Printf("%d %d",a, b)
}

func callback(y int, f func(int, int)) {
    f(y, 2)
}

// 用闭包进行调试
where := func() {
    _, file, line, _ := runtime.Caller(1)
    log.Printf("%s:%d", file, line)
}
where()

```
## Array
切片在内存中的组织方式实际上是一个有 3 个域的结构体：**指向相关数组的指针，切片 长度以及切片容量**。

**传递的都是值拷贝，或者是指针的值拷贝(联系切片,传递切片也包含相关数组的指针的拷贝),是值类型，但是表现出引用语义**

new(T) 为每个新的类型T分配一片内存，初始化为 0 并且返回类型为*T的内存地址：这种方法 返回一个指向类型为 T，值为 0 的地址的指针，它适用于值类型如数组和结构体（参见第 10 章）；它相当于 &T{}。
make(T) 返回一个类型为 T 的初始值，它只适用于3种内建的引用类型：切片、map 和 channel
```
func test(arr []int) {
    arr[0] +=1 //引用语义,arr虽然是切片拷贝,但是传递的是相关数组指针的拷贝，可以仍然可以修改原切片
    arr = []int{1,2,3,4}
}

var arr = new([5]int)
func test(arr *[5]int){ //传递数组指针,可以修改
    arr[0] +=1
}
```

## Map

```
//map初始化
var map1[keytype]valuetype = make(map[keytype]valuetype)
map1 := make(map[keytype]valuetype)
map1 := map[keytype]valuetype{}

```
## Struct

结构体嵌套

* 外层名字会覆盖内层名字（但是两者的内存空间都保留），这提供了一种重载字段或方法的方式；
* 如果相同的名字在同一级别出现了两次，如果这个名字被程序使用了，将会引发一个错误（不使用没关系）。没有办法来解决这种问题引起的二义性，必须由程序员自己修正。

Go 方法是作用在接收者（receiver）上的一个函数，接收者是某种类型的变量

## Interface

```
//类型断言,如果转换合法，v 是 varI 转换到类型 T 的值，ok 会是 true；否则 v 是类型 T 的零值，ok 是 false，也没有运行时错误发生。
v, ok := varI.(T)

//空接口 其他类型，向空接口类型拷贝
var dataSlice []myType = FuncReturnSlice()
var interfaceSlice []interface{} = make([]interface{}, len(dataSlice))
for ix, d := range dataSlice {
    interfaceSlice[ix] = d
}
```
