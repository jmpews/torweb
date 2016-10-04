# jmp

## 介绍

基于tornado并且有很多trick用法的社区.

#### Link: **[jmp](http://sxu.today)**

### 设计到的功能和模块:

#### 前端部分

* 标准化的前端构建流程(gulp+bower)
* 提供社区类型、展示类型、Blog类型的样式
* 注释详细的scss(部分组件样式引用bootstrap-v4)
* emoji支持
* 采用medium实现用户评论
* TinyMCE的富文本(加了一个支持粘贴上传的插件)
* 主题切换(通过DB和cookie两种方式以保证快速切换)

#### 后端部分

* 结构化项目组织
* 很多trick(缓存、异步...)
* 很多utils(时间友好化显示、安全参数获取...)
* 很多decorators(线程异步、peewee的连接释放、login_required)
* 社区功能
* 官方(个人)功能(PS: 可以将md直接导入数据库)
* websocket实现的多用户及时通讯
* 主题切换(通过DB和cookie两种方式以保证快速切换)

## 解决方案

把在写torweb遇到的问题，写成解决方案.

[websocket实时通讯解决.md](/docs/solutions/websocket实时通讯解决.md)

[头像裁剪上传解决方案.md](/docs/solutions/头像裁剪上传解决方案.md)

## TODO列表

#### 0. handler里设置
```
def get(self, *args, **kwargs):
	self.success()
```
#### 1. tornado+greenlet+decorators

## 安装&使用

完整安装过程 [docs/full-install.md](/docs/full-install.md) (基本不会出错)

```
# py3环境
source ~/virtualenv/python3.5.2/bin/active
git pull https://github.com/jmpews/torweb.git
# 依赖包
pip install -r requirements.txt
# 修改配置文件
vim settings/develoment.py
# 导入测试数据
python tests/test_mysql.py
# 启动服务
python app.py
```

## 组织架构
```
├── README.md
├── app/
│   ├── __init__.py
│   ├── api/
│   ├── cache.py # trick缓存
│   ├── index/
│   ├── post/
│   ├── recommend/
│   ├── registryauth/
│   ├── urls.py
│   ├── user/
│   └── utils/
├── app.py
├── custor/ # 自定义工具类、基础类等
│   ├── __init__.py
│   ├── auth.py
│   ├── errors.py # 自定义错误
│   ├── handlers/ # 自定义的基础handler
│   ├── logger.py # 自定义logger
│   ├── uimethods.py # 打到模板里的函数
│   └── utils.py # 工具类
├── db/ #数据model
│   ├── __init__.py
│   ├── mongo_db/
│   ├── mysql_model/
│   ├── redis_db/
│   └── torweb.sql
├── docs
│   └── solutions.md
├── frontend
│   ├── bower.json
│   ├── bower_components
│   ├── gulpfile.js # gulp文件
│   ├── node_modules
│   ├── package.json
│   ├── src # src文件
│   └── static
├── requirements.txt
├── settings
│   ├── __init__.py
│   ├── common.py # 通用基础配置文件
│   ├── config.py
│   ├── development.py # 开发配置文件
│   └── production.py # 生产配置文件
├── tests/ # 测试文件
│   ├── test_gen_couroutine.py
│   ├── test_mongo.py
│   ├── test_mysql.py
│   └── test_thread_future.py
└── tornado-generator.log # log文件
```
## 使用到的
```
MySQL, gulp, bower, pycharm, vim
```

## Tricks
### 0. Yield、Future与线程的结合，处理阻塞函数

把tornado的Future、Python里的Yield和线程结合起来，处理阻塞函数。可以查看`tests/test_thread_future.py` ，具体分析可以查看 http://jmpews.github.io/posts/tornado-future-ioloop-yield.html

```
from threading import Thread
class ThreadWorker(Thread):
    '''
    线程Future
    '''
    def __init__(self, future, func, *args, **kwargs):
        Thread.__init__(self)
        self.future =future
        self.func =func
        self.args = args
        self.kwargs = kwargs
        print('worker init...')

    def run(self):
        result = self.func(*self.args, **self.kwargs)
        self.future.set_result(result)

def run_with_thread_future(*args, **kwargs):
    '''
    如何利用yield, future和线程的配合
    http://jmpews.github.io/posts/tornado-future-ioloop-yield.html
    :param args:
    :param kwargs:
    :return:
    '''
    def wraps_func(func):
        @functools.wraps(func)
        def wraps_args(*args, **kwargs):
            future = Future()
            work = ThreadWorker(future, func, *args, **kwargs)
            work.start()
            return future
        return wraps_args
    return wraps_func
```
### 1. GET、POST、JSON参数获取
1. `get_cleaned_post_data_http_error` `get_cleaned_query_data_http_error` 获取参数，如果获取不到返回`HTTPError(400)`
2. `get_cleaned_query_data` `get_cleaned_post_data` 获取参数，返回自定义异常
3. `get_cleaned_json_data`获取json请求数据

```
def get_cleaned_query_data(handler, args, blank=False):
    '''
    这个是自定义异常的，然后到get/post去catch然后异常处理，不如raise HTTPError来的通用.
    '''
    data = {}
    for k in args:
        try:
            data[k] = handler.get_query_argument(k)
        except MissingArgumentError:
            if blank:
                data[k] = None
            else:
                raise RequestMissArgumentError('[' + k + '] arg not found')
    return data
```
### 2. 特殊缓存的实现

在`/app/cache.py` 缓存一些需要**面向所有用户使用**的缓存，比如缓存文章分类、热门文章分类、系统状态。当修改或者有新加的文章则进行主动更新。

```
# 当有很多用户访问时候，并不是每次都要查询系统状态，而是通过一个线程一直更新缓存(system_status_cache)，每个用户只要读取该数据缓存即可。

system_status_cache = [0, 0, 0, 0]

def update_system_status_cache():
    '''
    系统状态cache
    :return:
    '''
    from threading import Thread

    class MonitorWorker(Thread):
        '''
        监视系统状态线程
        '''
        def __init__(self, name, systatus):
            Thread.__init__(self)
            self.name = name
            self.systatus = systatus
        def run(self):
            logger.debug("start monitor system status...")
            import psutil, datetime, time
            while True:
                try:
                    time.sleep(30)
                    s1 = psutil.cpu_percent()
                    s2 = psutil.virtual_memory()[2]
                    try:
                        s3 = len(psutil.net_connections())
                    except:
                        s3 = 'unkown'
                    s4 = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d")
                    self.systatus[0] = s1
                    self.systatus[1] = s2
                    self.systatus[2] = s3
                    self.systatus[3] = s4
                except KeyboardInterrupt:
                    break

    monitor = MonitorWorker('system', system_status_cache)
    monitor.start()
    
update_system_status_cache()
```

### 3. GET、POST方法的异常装饰器
在get、post方法上添加装饰器，用于处理所有未捕获的异常，然后针对自定义异常调用已定义好方法处理。

```
def exception_deal(exceptions):
    '''
    捕获get, post函数异常
    :param exceptions:
    :return:
    '''
    def wrapper_func(func):
        # 保存原函数信息
        @functools.wraps(func)
        def wrapper_args(handler, *args, **kwargs):
            try:
                func(handler, *args, **kwargs)
            except Exception as ex:
                if isinstance(ex, PageNotFoundError):
                    handler.redirect(ex.redirect_url)
                elif isinstance(ex, RequestMissArgumentError):
                    handler.write(ex.msg)
                else:
                    raise ex
                # for e in exceptions:
                #     if isinstance(ex, e):
                #         handler.write('oh, catch exp in the args list...\n')
        return wrapper_args
    return wrapper_func
```

### 4. 用于计算get, post处理消耗时间的装饰器

```
def timeit(func):
    '''
    计算函数执行时间
    :param func:
    :return:
    '''
    def wrapper(*args, **kwargs):
        start = time.clock()
        func(*args, **kwargs)
        end = time.clock()
        # ColorPrint.print('> Profiler: '+func.__qualname__+'used: '+str((end - start) * 1e6) + 'us')
        ColorPrint.print('> Profiler: '+func.__qualname__+'used: '+str((end - start)) + 'us')
    return wrapper
```
### 5. 无闪切换主题
`db/mysql_model/user.py`

```
# 获取用户保存主题
def get_theme_by_cookie_user(self, handler):
   theme_color = handler.get_cookie('theme', '')
   if theme_color != '':
       return '.' + theme_color
   if self.theme:
       handler.set_cookie('theme', self.theme)
       return '.' + self.theme
   return ''
```
`fontend/static/templates/base.html`

```
{% if current_user %}
{% set theme = current_user.get_theme_by_cookie_user(handler) %}
<link id="theme" rel="stylesheet" type="text/css" href="/assets/css/index{{theme}}.css" />
    ...
```

### 6. 验证码模块,以及验证码装饰器

```
class CaptchaHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        captcha_str = random_captcha_str(4)
        captcha_data = image_captcha.generate(captcha_str)
        self.set_header("Content-type",  "image/png")
        # self.set_header('Content-length', len(image))
        self.set_cookie('captcha', captcha_str)
        self.write(captcha_data.getvalue())
        
def check_captcha(errorcode, result):
    """
    检查验证码 注意装饰器顺序
    :param errorcode:
    :param result:
    :return:
    """
    def wrap_func(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            captcha_cookie = self.get_cookie('captcha', '')
            captcha = get_cleaned_post_data(self, ['captcha'], blank=True)['captcha']
            if not captcha or captcha != captcha_cookie:
                self.write(json_result(errorcode, result))
                return
            return method(self, *args, **kwargs)
        return wrapper
    return wrap_func
```
## Features
### 1. 文件组织方面
```
├── app
│   ├── api/ # handler处理包含url, 最后集合所有url
│   │   ├── api.py
│   │   └── urls.py
```

方便前、后端开发
### 2. 多配置加载
通过`load_config`在所有模块之前加载配置文件，支持参数和环境变量两种方式(感觉有点复杂再考虑下)

```
def load_config(c):
    # global config

    from settings import development
    from settings import production

    if c:
        if c == 'production':
            config = development
        elif c == 'docker':
            pass
        else:
            config = production
    else:
        # load config from env
        envc = os.getenv('config', 'dev')
        if envc == 'production':
            config = production
        elif envc == 'docker':
            pass
        else:
            config = development
    return config
```
### 3. 采用数据库连接池
使用peewee作为连接驱动，需要做`request_hook`，在请求前申请数据库连接，请求完将连接放回连接池。

```
# 建立连接池
db_mysql = PooledMySQLDatabase(
        config.BACKEND_MYSQL['database'],
        max_connections=config.BACKEND_MYSQL['max_connections'],
        stale_timeout=config.BACKEND_MYSQL['stale_timeout'],  # 5 minutes.
        user=config.BACKEND_MYSQL['user'],
        password=config.BACKEND_MYSQL['password'],
        host=config.BACKEND_MYSQL['host'],
        port=config.BACKEND_MYSQL['port']
)
```

```
# request-hook
class BaseRequestHandler(RequestHandler):
    '''
    Peewee-Request-Hook-Connect
    '''

    def prepare(self):
        db_mysql.connect()
        return super(BaseRequestHandler, self).prepare()
    '''
    Peewee-Request-Hook-Close
    '''

    def on_finish(self):
        if not db_mysql.is_closed():
            db_mysql.close()
        return super(BaseRequestHandler, self).on_finish()
```
### 4. 工具类
#### logger
```
class Logger:
    '''
    自定义log
    '''
    def __init__(self, log_path, level=logging.DEBUG):
        self.logger = logging.getLogger(log_path)
        out_format = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

        file_log_handler = logging.FileHandler(log_path)
        file_log_handler.setFormatter(out_format)
        # file_log_handler.setLevel(level)

        steam_log_handler = logging.StreamHandler(sys.stdout)
        steam_log_handler.setFormatter(out_format)

        # steam_log_handler.setLevel(level)
        # self.logger.addHandler(steam_log_handler)
        self.logger.addHandler(file_log_handler)
        self.logger.setLevel(level)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)

    def exc(self, message):
        self.logger.exception(message)
```
#### 页数导航
```
def get_page_nav(current_page, page_number_limit, page_limit):
    '''
    页脚导航
    :param current_page:
    :param page_number_limit: 当前结果集的数据量
    :param page_limit: 每一页数据量
    :return:
    # 页导航(cp:当前页, <:前一页, >:后一页)
    # 模型: < cp-2, cp-1, cp, cp+1, cp+2A >
    # 这里如果换成列表存放，在模板里面会好操作一点
    '''
    pages = {'cp-2': 0, 'cp-1': 0, 'cp': current_page, 'cp+1': 0, 'cp+2': 0}
    #import pdb; pdb.set_trace()
    if current_page-1 >= 1:
        pages['cp-1'] = current_page-1
    if current_page-2 >= 1:
        pages['cp-2'] = current_page-2

    if (current_page)*page_limit < page_number_limit:
        pages['cp+1'] = current_page+1
    if (current_page+1)*page_limit < page_number_limit:
        pages['cp+2'][1] = current_page+2
    return pages
```
#### 时间友好显示
```
class TimeUtil:
    '''
    时间友好化显示
    '''
    @staticmethod
    def get_weekday(date):
        week_day_dict = {
            0: '星期一',
            1: '星期二',
            2: '星期三',
            3: '星期四',
            4: '星期五',
            5: '星期六',
            6: '星期日',
        }
        day = date.weekday()
        return week_day_dict[day]

    @staticmethod
    def datetime_format(value, format="%Y-%m-%d %H:%M"):
        return value.strftime(format)

    @staticmethod
    def datetime_format_date(value, format="%Y-%m-%d"):
        return value.strftime(format)

    @staticmethod
    def current_str_date():
        return time.strftime('%Y-%m-%d', time.localtime())

    @staticmethod
    def current_str_datetime():
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    @staticmethod
    def datetime_delta(t):
        now = datetime.datetime.now()
        time_date = now.date() - t.date()
        days = time_date.days
        seconds = (now - t).seconds
        # 星期一 8:00
        if days <= 6:
            if days < 1:
                if seconds < 60:
                    return '几秒前'
                elif seconds < 3600:
                    return '%s分钟前' % int(seconds / 60)
                else:
                    return TimeUtil.datetime_format(t, '%H:%M')
            if days < 2:
                return '昨天 ' + TimeUtil.datetime_format(t, '%H:%M')
            return TimeUtil.get_weekday(t) + ' ' + TimeUtil.datetime_format(t, '%H:%M')
        else:
            return TimeUtil.datetime_format(time, "%Y-%m-%d")
```
#### 控制台彩色打印
```
class ColorPrint:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def print(arg):
        print(ColorPrint.OKGREEN + arg + ColorPrint.ENDC)
```
#### Json格式化结果
```
def json_result(error_code, data):
    '''
    格式化结果为json
    :param error_code:
    :param data:
    :return:
    '''
    if isinstance(data, str):
        result = {'errorcode': error_code, 'txt': data}
    else:
        result = {'errorcode': error_code, 'data': data}
    return json.dumps(result)
```
#### login_required(from tornado)
```
def login_required(method):
    '''
    登陆 装饰器
    :param method:
    :return:
    '''
    from tornado.httpclient import HTTPError
    '''
    from "tornado.web.authenticated"
    `self.current_user`是一个@property
    '''

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)

    return wrapper
```

#### 添加websocket的相关实现

参考链接:

https://www.zhihu.com/question/20215561
