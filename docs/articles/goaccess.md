Title: 使用goaccess进行日志分析
Date: 2016-12-27 03:43
Author: jmpews
Category: tools
Tags: nginx
Slug: rgoaccess

# goaccess

## 安装

```
sudo apt-get install goaccess
```

## 配置

配置文件应该在 `/etc/goaccess.conf` 在配置添加, 关于具体相关配置, 请参考 `https://goaccess.io/man#custom-log`

```
time-format %T
date-format %d/%b/%Y
log-format %h %^[%d:%t %^] "%r" %s %b "%R" "%u"
```

## 分析日志

```
cat /var/log/nginx/torweb.access.log* | goaccess
```