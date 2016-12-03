Title: php基础笔记
Date: 2016-07-08 09:59
Author: jmpews
Category: php
Tags: php
Slug: study-php

## 类型
---
如果向八进制数传递了一个非法数字（即 8 或 9），则后面其余数字会被忽略。

### string

```
// 如果在数组定义中多个单元都使用了同一个键名，则只使用了最后一个，之前的都被覆盖了。
// 如果对给出的值没有指定键名，则取当前最大的整数索引值，而新的键名将是该值加一。如果指定的键名已经有了值，则该值会被覆盖。
<?php
$array = array(
    1    => "a",
    "1"  => "b",
    1.5  => "c",
    true => "d",
);
var_dump($array);
?>

// Output:
array(1) {
  [1]=>
  string(1) "d"
}
```

```
$a = array();
$a['color'] = 'red';
$a['taste'] = 'sweet';
$a['shape'] = 'round';
$a['name']  = 'apple';
$a[]        = 4;        // key will be 0
```

```
<?php
// 创建一个简单的数组
$array = array(1, 2, 3, 4, 5);
print_r($array);

// 现在删除其中的所有元素，但保持数组本身不变:
foreach ($array as $i => $value) {
    unset($array[$i]);
}
print_r($array);

// 添加一个单元（注意新的键名是 5，而不是你可能以为的 0）
$array[] = 6;
print_r($array);

// 重新索引：
$array = array_values($array);
$array[] = 7;
print_r($array);
?>
```

因为 PHP 自动将裸字符串（没有引号的字符串且不对应于任何已知符号）转换成一个其值为该裸字符串的正常字符串。例如，如果没有常量定义为 bar，PHP 将把它替代为 'bar' 并使用之。

使用引用运算符(&)通过引用来拷贝数组

## 变量
---
### 可变变量
```
<?php
$$a = 'world';
?>

<?php
echo "$a ${$a}";
?>
```
