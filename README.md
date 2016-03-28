# Tornado项目Generator

## Web框架
Tornado(Python3)

## 设计特点:

### DB使用:
Mongo做session存储、服务器stats(url访问统计)

Reis做访问频率限制以及cache缓存(访问速率其实可以在nginx进行控制,见附)

Mysql做DataDB

### LOG及异常处理
重写`requesthandler`的`write_error`，返回500.html

添加`default_handler_class`，处理404，并做好LOG

### 参数安全处理
对参数进行clean

### Mysql设计
#### peewee
使用peewee做为driver,虽然使用了connectionpool但是没有添加RequestHook(在请求来时创建连接，请求结束释放),如果使用可能需要调节这里

### Mongo设计
#### 用户Session
`{ "_id" : "encrypt_id", "data" : { "key" : "value" } }`

Ex: `{ "_id" : "Km9hAb58ePjV9NdJtBR0lxNMmSPfe6e3Kmi43n6gsDMp1GTWet8wHS3mYjcX6g", "data" : { "openid" : "test" } }`

### Redis设计
#### 用户访问频率限制
`'ratelimit:ip':count`

Ex: `'ratelimit:127.0.0.1':5` & `expire(5)`

### 封装好的handler

`Adv__BaseRequestHandler` session和url访问记录handler

`Rate_BaseRequestHandler` 访问频率处理handler

## 使用&测试

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

# create tables
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

## 附录

### Nginx配置文件
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
