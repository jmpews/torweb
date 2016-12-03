Title: SSH笔记
Date: 2015-10-27 00:01
Author: jmpews
Category: linux/shell
Tags: ssh
Slug: use-ssh
Summary: 了解SSH以及socks5

## SSH本地端口转发。

`ssh -L 2121:host2:21 host3`ssh建立一个socket绑定本地2121端口，通过host3这个桥，转发本地2121端口请求到host2:21

## SSH远程端口转发

host3在内网，可以访问外网host1

`ssh -R 2121:host2:21 host1`建立socket连接host1:2121，让host1监听2121端口，让所有数据转发到host2:21

前提，host1和host3两台主机都有sshD和ssh客户端。

## 额外参数

-N参数，表示只连接远程主机，不打开远程shell；T参数，表示不为这个连接分配TTY。这个两个参数可以放在一起用，代表这个SSH连接只用来传数据，不执行远程操作。f参数，表示SSH连接成功后，转入后台运行。


### http隧道
分为不使用connect的隧道和使用connect的隧道，不用connect的隧道为重新组装请求，而https必须通过connect建立隧道通信

### 端口映射
将来自指定外网IP的某一端口的请求转发到内网某一IP的某一个端口

#### iptables的端口转发
```
# 使用iptables实现端口转发
echo 1 > /proc/sys/net/ipv4/ip_forward
iptables -t nat -I PREROUTING -p tcp –dport 80 -j DNAT –to xx.xx.xx.xx
iptables -t nat -I POSTROUTING -p tcp –dport 8080 -j MASQUERADE
service iptables save
```
#### ssh的本地端口转发和远程端口转发
[ssh隧道、端口转发、内网穿透](http://blog.creke.net/722.html)
