Title: python中的元类
Date: 2016-10-17 11:12
Author: jmpews
Category: python
Tags: python, 元类
Slug: python-metaclass

### 什么是元类?

```
class Test():
    fool = 1

t = Test()

print(type(t))
print(type(Test))
print(type(type))
```

** t 是 Test 类的实例, 那么 Test 又是谁的实例? **

** t 的类型是 Test, 那么 Test 的类型是什么? **

**Test 是 type 的实例.**

**type 就是元类.**

### 动态生成类
```
type(name of the class,
    tuple of the parent class (for inheritance, can be empty),
    dictionary containing attributes names and values)

# Example
type('Test', (), {'fool': 1})
```

### 自定义元类

```
class Test(type):
    def __new__(cls, clsname, bases, dct):
        attrs = {}
        for name, val in dct.items():
            if name == 'fool':
                attrs[name] = 1
        return type.__new__(cls, clsname, bases, attrs)
```

### 使用元类实现ORM

> Foo中有metaclass这个属性吗？如果是，Python会在内存中通过metaclass创建一个名字为Foo的类对象（我说的是类对象，请紧跟我的思路）。如果Python没有找到metaclass，它会继续在Bar（父类）中寻找metaclass属性，并尝试做和前面同样的操作。如果Python在任何父类中都找不到metaclass，它就会在模块层次中去寻找metaclass，并尝试做同样的操作。
> 如果还是找不到metaclass,Python就会用内置的type来创建这个类对象。

实现如下功能的ORM

```
class User(Model):
    # 定义类的属性到列的映射：
    id = IntegerField('id')
    name = StringField('username')
    email = StringField('email')
    password = StringField('password')

# 创建一个实例：
u = User(id=12345, name='Michael', email='test@orm.org', password='my-pwd')

# 保存到数据库：
# metaclass的发挥作用
u.save()
```

具体实现

```
class StringField(Field):

    def __init__(self, name):
        super(StringField, self).__init__(name, 'varchar(100)')

class IntegerField(Field):

    def __init__(self, name):
        super(IntegerField, self).__init__(name, 'bigint')

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k, v in attrs.items():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.keys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def save(self):
        fields = []
        params = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v.name)
            params.append('?')
            args.append(getattr(self, k, None))
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(args))
```

### 参考

参考链接:

https://github.com/xiyoulaoyuanjia/blog/blob/master/%E7%90%86%E8%A7%A3python%E4%B8%AD%E7%9A%84%E5%85%83%E7%B1%BB.md

http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014319106919344c4ef8b1e04c48778bb45796e0335839000
