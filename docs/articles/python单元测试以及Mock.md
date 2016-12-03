Title: Python单元测试以及Mock
Date: 2016-04-24 11:12
Author: jmpews
Category: python
Tags: python,mock
Slug: python-unittest-mock

## Summary(基本单元测试):

* 测试可以保证你的代码在一系列给定条件下正常工作(**e:保证基本功能正确**)
* 测试允许人们确保对代码的改动不会破坏现有的功能(**e:保证在修改的过程中,功能不变**)
* 测试迫使人们在不寻常条件的情况下思考代码，这可能会揭示出逻辑错误(**e:传入不同参数或边界参数**)
* 良好的测试要求模块化，解耦代码，这是一个良好的系统设计的标志(**e:模块化设计**)

通过一段代码来对比上面

```
import unittest


def double_div(a, b):
    return a / b / b


class TestBase(unittest.TestCase):
    def setUp(self):
        '''
        Test之前的初始化
        '''
        self.a = 4
        self.b = 2

    def test_double_div_default(self):
        self.assertEqual(1, double_div(self.a, self.b), 'Not 1')

    def test_double_div_1_2(self):
        self.assertEqual(0.04, double_div(1, 5), 'Not 0.04')

    def test_double_div_1_2_double(self):
        self.assertEqual(0.04, double_div(1.0, 5), 'Not 0.04')

    def test_double_div_1_0(self):
        self.assertEqual(0, double_div(1, 0), 'Not 0')


if __name__ == '__main__':
        unittest.main()

```

结果:

```
$ python python_unittest.py
EF..
======================================================================
ERROR: test_double_div_1_0 (__main__.TestBase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "python_unittest.py", line 28, in test_double_div_1_0
    self.assertEqual(0, double_div(1, 0), 'Not 0')
  File "python_unittest.py", line 7, in double_div
    return a / b / b
ZeroDivisionError: integer division or modulo by zero

======================================================================
FAIL: test_double_div_1_2 (__main__.TestBase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "python_unittest.py", line 22, in test_double_div_1_2
    self.assertEqual(0.04, double_div(1, 5), 'Not 0.04')
AssertionError: Not 0.04

----------------------------------------------------------------------
Ran 4 tests in 0.000s
```

## Mock测试

基本用法说就是'模拟伪造'对象，模仿这个对象的返回值、属性等。这样可以避免一些副作用和耗时操作，比如:删除文件(remove)等

```
import unittest
import mock
import requests
import json


def get_name(uuid):
    r = requests.get('http://example.com')
    user_name = json.loads(r.text)
    return user_name


def check_user_info(uuid):
    print(uuid)
    username = get_name(uuid)
    print(username)
    if username == 'admin':
        return True
    else:
        return False


class TestUserInfo(unittest.TestCase):
    def setUp(self):
        self.uuid = '1234'

    @mock.patch('__main__.get_name')
    def test_check_user_info(self, mock_get_name):
        mock_get_name.return_value = 'jmpews'
        result = check_user_info(self.uuid)
        mock_get_name.assert_called_once_with(self.uuid)
        self.assertTrue(result, msg='> Check False!')


if __name__ == '__main__':
    unittest.main()
```
### 参考文章:
---
[Python3.4的unittest.mock官方文档](https://docs.python.org/3.4/library/unittest.mock-examples.html)

[Python Mock的入门(很详细,推荐)](https://segmentfault.com/a/1190000002965620)

[Python中如何创建mock?](http://code.oneapm.com/python/2015/06/11/python-mock-introduction/)
