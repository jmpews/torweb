Title: Django ORM笔记
Date: 2015-11-27 03:43
Author: jmpews
Category: django
Tags: python, django
Slug: django-orm

### `__`神奇用法

```
多表联合查询,可用通过可以通过poc表访问vul外键对应的vul表中的字段
poc.objects.values('id','vul__name').all()
```

### 外键关系反查

```
# 设置关系叫做`re_demand`
class Demand(models.Model):
  submitter = models.ForeignKey(User, verbose_name=u"需求提交者",related_name='re_demand')
class User(models.Model):
  name=models.CharField()

# 获取该user对应的所有demands
user.re_demand.all()
```
