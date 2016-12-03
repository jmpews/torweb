Title: Tornado项目模板
Date: 2016-4-10 03:43
Author: jmpews
Category: tornado
Tags: tornado
Slug: tornado-project-generator

最近写了一个tornado的项目模板生成器。可以快速生成tornado项目，从后端DB、日志记录、session控制、参数清理等都做了比较好的封装。github:[tornado-project-generator](https://github.com/jmpews/tornado-project-generator)。

首先这个框架是基于Py3的，但其实Py2稍微改下就能用。

### 1.DB相关处理

Mongo做session存储、服务器stats(例如url访问统计)

Reis做访问频率限制以及cache缓存(访问速率其实可以在nginx进行控制,见附)

MySQL做DB存储

(可能并不需要这么多)

#### MySQL
##### peewee

使用peewee做为driver,虽然使用了connectionpool但是没有添加RequestHook(在请求来时创建连接，请求结束释放),如果使用可能需要调节这里。

**创建数据库需要设置好编码**

#### Redis
##### 用户访问频率限制
封装了几个处理的handler

`'ratelimit:ip':count`

Example: `'ratelimit:127.0.0.1':5` & `expire(5)`

#### Mongo
#### 用户Session
`{ "_id" : "encrypt_id", "data" : { "key" : "value" } }`

Example: `{ "_id" : "Km9hAb58ePjV9NdJtBR0lxNMmSPfe6e3Kmi43n6gsDMp1GTWet8wHS3mYjcX6g", "data" : { "openid" : "test" } }`

### 2.utils相关封装

#### 参数安全获取

```
def get_cleaned_post_data(handler,args,blank=False):
    '''
    这个是自定义异常的，然后到get/post去catch然后异常处理，亦可以raise HTTPError来的通用。
    '''
    data={}
    for k in args:
        try:
            data[k]=clean_data(handler.get_body_argument(k))
        except MissingArgumentError:
            if blank:
                data[k]=None
            else:
                raise RequestArgumentError(k+' arg not found')
    return data
```
可以post方法里这样获取参数`post_data=get_cleaned_post_data(self,['username','password'])`

对于异常有两种处理:

(1).`try:catch`自定义处理异常

```
try:
    post_data=get_cleaned_post_data(self,['username','password'])
except RequestArgumentError as e:
    self.write(json_result(e.code,e.msg))
    return
```

(2).不做自定义处理,错误被抛到`BaseRequestHandler`的`write_error`，在那里做统一处理

```
class BaseRequestHandler(RequestHandler):
    '''
    重写了异常处理
    '''
    def write_error(self, status_code, **kwargs):
        if 'exc_info' in kwargs:
            # 参数缺失异常
            if isinstance(kwargs['exc_info'][1],RequestArgumentError):
                self.write(json_result(kwargs['exc_info'][1].code,kwargs['exc_info'][1].msg))
                return

        if status_code==400:
            self.write(json_result(400,'缺少参数'))
            return
        if not config.DEBUG:
            self.redirect("/static/500.html")
```

#### 登陆(loginrequired)
```
def login_required(method):
    from tornado.httpclient import HTTPError
    '''
    取自"tornado.web.authenticated"
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

### 使用&测试

安装requirements.txt
```
pip install -r requirements.txt
```

mysql配置
```
# create database
CREATE DATABASE tornado
  DEFAULT CHARACTER SET utf8
  DEFAULT COLLATE utf8_general_ci;

# 创建基本数据库
python tests/test_mysql.py
```

redis安全配置
```
bind 127.0.0.1
```

mongo安全配置
```
net:
  port: 27017
  bindIp: 127.0.0.1
```

`python app.py -port=8001`

默认用户(`test_mysql.py`) `{username: admin,password: root}`

### 附录

#### Nginx配置文件
```
user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections 1024;
}

http {
    upstream frontends {
        server 127.0.0.1:8001;
        server 127.0.0.1:8002;
    }

    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;

    keepalive_timeout 65;
    proxy_read_timeout 200;
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    gzip on;
    gzip_min_length 1000;
    gzip_proxied any;
    gzip_types text/plain text/css text/xml
               application/x-javascript application/xml
               application/atom+xml text/javascript;


    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    # rate limit:分配10m的zone,每秒5次上限
    limit_req_zone $binary_remote_addr zone=allips:10m rate=5r/s;
    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include /etc/nginx/conf.d/*.conf;

    server {
        listen 80;
        server_name  weixin.linevery.com;

        # 桶控制
        limit_req zone=allips burst=2 nodelay;

        client_max_body_size 50M;

        location ^~ /static/ {
            # 根目录文件
            root /home/jmpews/sxuhelp;
            if ($query_string) {
                expires max;
            }
        }
        location = /favicon.ico {
            rewrite (.*) /static/favicon.ico;
        }
        location = /robots.txt {
            rewrite (.*) /static/robots.txt;
        }

        location / {
            proxy_pass_header Server;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Scheme $scheme;
            proxy_pass http://frontends;
        }
    }
}
```
