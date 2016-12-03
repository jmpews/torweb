Title: nginx基础笔记
Date: 2016-10-18 09:59
Author: jmpews
Category: nginx
Tags: nginx
Slug: nginx-note

### nginx设置日志格式

```
# log_format 日志名字 日志格式
log_format  torweb  '$host $remote_addr - $remote_user [$time_local] "$request" '
					'$status $body_bytes_sent "$http_referer" '
					'"$http_user_agent" "$http_x_forwarded_for"';

# 使用特定日志格式
access_log  /usr/local/var/log/nginx/torweb.access.log torweb;
```

### nginx正则重定向

需要实现一个需求: 对于特定的域名访问, 自动跳转到指定的路由, 访问其他路由自动跳到该路由

比如: 访问 `jmpews.com` 自动跳转到 `jmpews.com/blog`, 然而对于 `jmpews.com/blog` 不再进行正则处理. 

这里用到几个知识.

1. 正则的零宽断言(`(?=blog)`) 

2. 德摩根定: `¬(p∧q)≡¬p∨¬q	¬(p∨q)≡¬p∧¬q` (`((v2)|(assets)|(blog))`)

```
if ($host ~* '(www\.)?jmpews\.me') {
	rewrite '^(?!/((v2)|(assets)|(blog))/).*' /blog break;
}
```

参考:

http://www.isnowfy.com/regular-expression-negative/

http://ued.fanxing.com/2016/09/30/nginx_location_rewrite/
