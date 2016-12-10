Title: Zmap笔记
Date: 2016-06-09 09:12
Author: jmpews
Category: scan
Tags: zmap
Slug: zmap-tool

> https://github.com/zmap/zmap

> https://zmap.io/documentation.html

## 安装
```
cmake -DWITH_REDIS=OFF -DENABLE_DEVELOPMENT=ON .
```
---

## 扫描
#### 基本的扫描方式
```
sudo zmap -p 80 -o results.csv 114.215.105.0/24
```

#### 使用配置文件进行扫描
```
probe-module tcp_synscan
target-port 80

output-module csv
output-file zmap-output-80.csv
output-filter "success = 1 && repeat = 0"
output-fields "saddr,daddr,sport,seqnum,acknum,cooldown,repeat,timestamp-str"

#Gateway MAC address to send packets to (in case auto-detection does not work)
#gateway-mac addr

# see the packets that would be sent over the network
# dryrun

# Level of log detail
verbosity 3

# finish summary
metadata-file zmap-80-metadata.json

# zmap log
log-file zmap-80.log

# zmap status
status-updates-file zmap-status.txt
```
---

## 参考资料

[Github-Issue] https://github.com/zmap/zmap/issues (比如:summary选项已经移除、使用metadata-file代替)

[不错的资料] https://linux.cn/article-5860-1.html#probemodule

[官方Doc] https://zmap.io/documentation.html

[Man] `man zmap`
