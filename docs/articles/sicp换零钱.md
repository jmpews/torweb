Title: sicp换零钱-递归转尾递归
Date: 2016-07-12 03:43
Author: jmpews
Category: SICP
Tags: 递归,迭代
Slug: sicp-make-change

递归和迭代的转化，关键需要明确哪些是递归的冗余数据，也就说哪些是迭代可以重复利用数据。下面具体分析。

给不同的coin分配索引

```
(define (first-denomination kinds-of-coins)
    (cond ((= kinds-of-coins 1) 1)
        ((= kinds-of-coins 2) 5)
        ((= kinds-of-coins 3) 10)
        ((= kinds-of-coins 4) 25)
        ((= kinds-of-coins 5) 50)))

```

### 递归的思路

将总数为a的现金换成n种硬币的不同方式的数目等于

1. 将现金a换成除第一种硬币以外的其他硬币的不同方式，加上2
2. 将现金a－d换成所有种类硬币的不同方式。其中d为第一种硬币的面值。

可以写递归公式

`Ct(N) = Ct(N-first-denomination(t)) + Ct-1(N)`

t(下标)为几种硬币，N为现金数。例如：t为5，N为100美分，所以总数目=(将100美分换成1,5,10,25这四种硬币组成方法数)+(将100-50美分换成1,5,10,25,50这五种硬币组成的方法数)

通过公式进行初步运算，渐渐会发现冗余数据(重复利用的数据)

```
C5(100)=C4(100)+C5(50)
    C4(100)==C3(100)+C4(75)
        C3(100)=C2(100)+C3(90)
            C2(100)=C1(100)+C2(95)
                C2(95)=C1(95)+C2(90)
                    C2(90)=C1(90)+C2(85)
                        C2(85)=C1(85)+C2(80)
                            C2(80)=C1(80)+C2(75)
                                C2(75)=C1(75)+C2(70)
                                    ...
            # C2(90) 重复
            C3(90)=C2(90)+C3(80)
                # C2(80) 重复
                C3(80)=C2(80)+C3(70)
                    # C2(70) 重复
                    C3(70)=C2(70)+C3(60)
                        ...
        C4(75)=C3(75)+C4(50)
            C3(75)=C2(75)+C3(65)
                ...
            C4(50)=C3(50)+C4(25)
                ...
    C5(50)=C4(50)+C5(0)
        C5(50)=C4(50)+C5(0)
            ...
```

上面可能不太直观

```
C2(4) = C1(4) + C2(-1)
C2(5) = C1(5) + C2(0)
C2(6) = C1(6) + C2(1)
C2(7) = C1(7) + C2(2)
C2(8) = C1(8) + C2(3)
C2(9) = C1(9) + C2(4) //出现重复利用值C2(4) 间隔为5
C2(10) = C1(10) + C2(5) //出现重复利用值C2(5) 间隔为5
C2(11) = C1(11) + C2(6)
C2(12) = C1(12) + C2(7)
C2(13) = C1(13) + C2(8)
C2(14) = C1(14) + C2(9)
C2(15) = C1(15) + C2(10)
C2(16) = C1(16) + C2(11)


C3(4) = C2(4) + C3(-6)
C3(5) = C2(5) + C3(-5)
C3(6) = C2(6) + C3(-4)
C3(7) = C2(7) + C3(-3)
C3(8) = C2(8) + C3(-2)
C3(9) = C2(9) + C3(-1)
C3(10) = C2(10) + C3(0)
C3(11) = C2(11) + C3(1)
C3(12) = C2(12) + C3(2)
C3(13) = C2(13) + C3(3)
C3(14) = C2(14) + C3(4) //出现重复利用值C3(4) 间隔为10
C3(15) = C2(15) + C3(5) //出现重复利用值C3(5) 间隔为10
C3(16) = C2(16) + C3(6)
```

**所以对于C2来说，始终需要缓存5个可以重复利用值(长度为5的缓存队列);对于C3，始终需要缓存10个可以重复利用值(长度为10的缓存队列);对于C4，使用需要缓存25个(...);对于C5来说，使用需要缓存50个可以重复利用值(...)**

### 迭代思路

1. 迭代是线性O(n)时间+常量空间消耗(不会随n改变)
2. 迭代需要**重复利用**递归产生的冗余数据.
3. 迭代的状态能由这些变量完全刻画

假设有5种硬币，现金100美分

C 源码

```
/*
 * =====================================================================================
 *
 *  Filename:  p26.c
 *
 *  Description: change money
 *
 *  Version:  1.0
 *  Created:  2016/08/02 14时58分22秒
 *  Revision:  none
 *  Compiler:  gcc
 *
 *  Author:  jmpews (jmpews.github.io), jmpews@gmail.com
 *
 * =====================================================================================
 */


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int count_change(int amount);
int cc(int amount, int kinds_of_coins);
void count_iter(int *tmp, int t, int amount);
int get_coin(int index_of_coin);
int get_index_tmp(int index_of_coin);
int *get_tmp_array(int kinds_of_coins);
int get_recycle_value(int index_of_coin, int current_amount, int *tmp_array);
void update_recycle_value(int index_of_coin, int *tmp_array, int value);

int main ( int argc, char *argv[] )
{
    int t;
    t = count_change(100);
    printf("%d", t);
    return EXIT_SUCCESS;
}				/* ----------  end of function main  ---------- */

int count_change(int amount) {
    cc(amount, 5);
    return 0;
}

int cc(int amount, int kinds_of_coins) {
    int *tmp = get_tmp_array(kinds_of_coins);
    int t = 0;
    tmp[0] = 0;
    count_iter(tmp, t, amount);
    return 0;
}

// 这里这里也是关键点，这个尾递归的结束由t(当前需要兑换的金钱)和amount(需要兑换的目标金钱)控制，为线性，也就是说时间复杂度为O(n)
void count_iter(int *tmp, int t, int amount) {
    int r;
    r = get_recycle_value(1, t, tmp);
    update_recycle_value(1, tmp, r);

    //C2(t) = C2(t-get_coin(2)) + C1(t)
    r = get_recycle_value(2, t, tmp) + r;
    update_recycle_value(2, tmp, r);

    //C3(t) = C3(t-get_coin(3)) + C2(t)
    r = get_recycle_value(3, t, tmp) + r;
    update_recycle_value(3, tmp, r);

    //C4(t) = C4(t-get_coin(4)) + C3(t)
    r= get_recycle_value(4, t, tmp) + r;
    update_recycle_value(4, tmp, r);

    //C5(t) = C5(t-get_coin(5)) + C4(t)
    r = get_recycle_value(5, t, tmp) + r;
    if(t == amount) {
        printf("final-value: %d\n", r);
        exit(1);
    }
    update_recycle_value(5, tmp, r);

    count_iter(tmp, t+1, amount);
}

int get_coin(int index_of_coin) {
    switch(index_of_coin) {
        case 1: return 1;
        case 2: return 5;
        case 3: return 10;
        case 4: return 25;
        case 5: return 50;
        default: exit(1);
    }
}

// 对于C1、C2、C3、C4、C5缓存队列开始的位置
int get_index_tmp(int index_of_coin) {
    switch(index_of_coin) {
        case 1: return 0;
        case 2: return 1;
        case 3: return 6;
        case 4: return 16;
        case 5: return 41;
        default: exit(1);
    }
}

// 分配固定的缓存, 无论需要兑换多少金钱，只要金币种类不变，缓存的大小就是固定的。 空间复杂度为常量。
// "因为它的状态能由其中的三个状态变量完全刻画，解释器在执行 这一计算过程时，只需要保存这三个变量的轨迹就足够了" 这句话在这里就有体现了
int *get_tmp_array(int kinds_of_coins) {
    int *tmp;
    int i;
    int sum = 0;
    for(i=1 ; i<kinds_of_coins ; i++) {
        sum += get_coin(i);
    }
    tmp = (int *)malloc(sizeof(int) * sum);
    memset(tmp, 0 ,sizeof(int) * sum);
    return tmp;
}

// 获取重复利用值, 每次缓存队列头的位置
// 比如: 此时缓存队列为[C2(0), C2(1), C2(2), C2(3), C2(4)]
// C2(5) = C1(5) + C2(0) 此时我们需要取缓存队列头的值C2(0)
// 计算完得到C2(5)，需要执行update_recycle_value将得到C2(5)进队列，除去旧的C2(0)，此时队列头尾C2(1)，即为计算C2(6)需要的缓存值
int get_recycle_value(int index_of_coin, int current_amount, int *tmp_array) {
    int t = get_index_tmp(index_of_coin);
    if(current_amount < get_coin(index_of_coin)){
        return 0;
    }
    else if(current_amount == get_coin(index_of_coin)){
        return 1;
    }
    else {
        return tmp_array[t];
    }
}

// 更新重复利用值(队列的概念), 计算出最新的值，需要替换旧的利用值
// 比如: C2(5) = C1(5) + C2(0)
// 现在C2缓存队列中有[C2(0), C2(1), C2(2), C2(3), C2(4)]，我们需要将C2(5)进队列，[C2(1), C2(2), C2(3), C2(4), C2(5)]
void update_recycle_value(int index_of_coin, int *tmp_array, int value) {
    int i;
    int t = get_index_tmp(index_of_coin);
    for(i = 0; i< (get_coin(index_of_coin)-1); i++) {
        tmp_array[t+i] = tmp_array[t+i+1];
    }
    tmp_array[t+get_coin(index_of_coin)-1] = value;
}
```

### 参考
http://stackoverflow.com/questions/1485022/sicp-making-change/
