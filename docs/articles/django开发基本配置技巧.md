Title: django开发基本配置技巧
Date: 2015-11-03 03:43
Author: jmpews
Category: django
Tags: django, python
Slug: study-django

## 入门配置篇

```
#模板
'DIRS': [BASE_DIR+"/templates",]

#新建数据库
python manage.py migrate
python manage.py makemigrations

#数据库相关操作
list = Test.objects.all()
Test.objects.filter(id=1)
Publisher.objects.order_by("name")
Publisher.objects.order_by("state_province", "address")
#相当于limit10
Publisher.objects.order_by('name')[10]

#批量update
Publisher.objects.filter(id=52).update(name='Apress Publishing')

#批量删除   
Publisher.objects.filter(country='USA').delete()

#从数据提取数据
try:
    p = Publisher.objects.get(name='Apress')
except Publisher.DoesNotExist:

#django admin管理,字符型可以仅仅使用blank，而一些以其他数据，需要加上null
publication_date = models.DateField(**blank=True, null=True** )

#model降序
class Article(models.Model):
    class Meta:  #按时间下降排序
        ordering = ['-date_time']


#变量描述
forloop.counter 索引从 1 开始算
forloop.counter0 索引从 0 开始算
forloop.revcounter 索引从最大长度到 1
forloop.revcounter0 索引从最大长度到 0
forloop.first 当遍历的元素为第一项时为真
forloop.last 当遍历的元素为最后一项时为真
forloop.parentloop 用在嵌套的 for 循环中，

```

## Admin基本配置

```
#每一个条目显示的字段
list_display = ('first_name', 'last_name', 'email')
#每一个条目支持修改的字段
fields = ('title', 'authors', 'publisher')
```

## Django下URLconf配置
### 1.使用命名组参数

```
urlpatterns = patterns('',
    # 命名组参数year,month
    (r'^articles/(?P<year>\d{4})/$', views.year_archive),
    (r'^articles/(?P<year>\d{4})/(?P<month>\d{2})/$', views.month_archive),
)
```

### 2.传递额外参数

增加了URL和Views的耦合度

```
# 不好！！！！ 增加了URL和Views的耦合度
urlpatterns = patterns('',
    (r'^(foo)/$', views.foobar_view),
    (r'^(bar)/$', views.foobar_view),
)

def foobar_view(request, url):
    m_list = MyModel.objects.filter(is_new=True)
    if url == 'foo':
        template_name = 'template1.html'
    elif url == 'bar':
        template_name = 'template2.html'
    return render_to_response(template_name, {'m_list': m_list})
```

传递额外参数

```
urlpatterns = patterns('',
    # 传递了额外参数,template_name
    (r'^foo/$', views.foobar_view, {'template_name': 'template1.html'}),
    (r'^bar/$', views.foobar_view, {'template_name': 'template2.html'}),
)

def foobar_view(request, template_name):
    m_list = MyModel.objects.filter(is_new=True)
    return render_to_response(template_name, {'m_list': m_list})
```

伪造URLconf参数

```
urlpatterns = patterns('',
    # 对于特例情况下，伪造urlconf
    (r'^mydata/birthday/$', views.my_view, {'month': 'jan', 'day': '06'}),
    (r'^mydata/(?P<month>\w{3})/(?P<day>\d\d)/$', views.my_view),
)
```
额外参数优先级要高对于捕获参数的优先级

url匹配存在短路逻辑

从url提取的所有参数均为文本

### post和get分给不同函数处理
```
# 这里的参数，*args列表类型,**kwargs字典类型
def method_splitter(request, *args, **kwargs):
    get_view = kwargs.pop('GET', None)
    post_view = kwargs.pop('POST', None)
    if request.method == 'GET' and get_view is not None:
        return get_view(request, *args, **kwargs)
    elif request.method == 'POST' and post_view is not None:
        return post_view(request, *args, **kwargs)
    raise Http404
```

### 装饰器(访问很多页面要求已经登陆)
```
# 可以做成装饰器
def requires_login(view):
    def new_view(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect('/accounts/login/')
        return view(request, *args, **kwargs)
    return new_view
```

## 渲染模板
RequestContext可以包含req参数，同时可以将这个请求过程中一直存在的参数放到其中，相比Context而言。

```
def custom_proc(request):
    "A context processor that provides 'app', 'user' and 'ip_address'."
    return {
        'app': 'My app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']
    }

def view_1(request):
    return render_to_response('template1.html',
        {'message': 'I am view 1.'},
        # 多个视图通用的参数
        context_instance=RequestContext(request, processors=[custom_proc]))
```

### 关闭模板自转义
```
{% autoescape off %}
    Hello {{ name }}
{% endautoescape %}
```
### url规则名字，自动更改前缀
```
url(r'^add/(\d+)/(\d+)/$', 'app.views.add', name='add'),
{% url 'some-url-name' arg arg2 as the_url %}
```

## Model高级

### 1.增加数据库manager方法
```
class BookManager(models.Manager):
    def title_count(self, keyword):
        return self.filter(title__icontains=keyword).count()
    #修改初始Manager QuerySets
    def get_query_set(self):
        return super(DahlBookManager, self).get_query_set().filter(author='Roald Dahl')

class Book(models.Model):
    ...
    objects = BookManager()
    roald_objects=BookManager()
```

### 2.用户model自定义

https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model

`AbstractBaseUser` 是全部定制，需要重写覆盖`BaseUserManager`,`BaseUserAdmin`

`AbstractUser` 如果只是扩展字段可以用这个
