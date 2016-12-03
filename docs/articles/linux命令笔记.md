Title: Linux命令笔记
Date: 2016-2-27 03:43
Author: jmpews
Category: linux
Tags: linux
Slug: linux-cmd-note

## lsof

```
#查看所有已经建立的TCP连接(不解析port和host)
lsof -i -sTCP:ESTABLISHED -P -n

#查看某个进程打开文件
lsof -p pid

#查看TCP链接状态
lsof -iTCP -sTCP:ESTABLISHED

#查看某个端口的的连接
lsof -i :22
```

## find

```
查找文件夹下包含某字符串的所有文件
find ./ |xargs grep -ri "str"
```
## ps

```
查看运行参数
ps -ef |grep mysql
```

## sudo

```
以某一个用户权限执行命令
sudo -u apache ls
```

## /etc/group & /etc/passwd

```
# /etc/group 文件详解

#第一字段:用户组名称
#第二字段:用户组密码
#第三字段:GID
#第四字段:用户列表,每个用户之间用,号分割;本字段可以为空,如果字段为空表示用户组为GID的用户名

# 用户组root,没有口令,包含用户root,me以及GID为0的用户(可以通过/etc/passwd查看)
root:x:0:root,me
```
## grep
```
# 查找包含指定字符串的文件
grep -n ` find -name "*.go"` -e "ErrTooLong"
```

## wc
```
# 返回文件行数
wc -l filename
```
## nc
```
# 监听本地8001端口，打印请求
nc -l 8001

# 发送字符串
echo 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e | nc -vvn 127.0.0.1 30000
```

## tcp
```
# https://en.wikipedia.org/wiki/Transmission_Control_Protocol
# https://zh.wikipedia.org/wiki/IPv4
# 根据'Data offset'得到TCP-Length, 判断此后四个字节是否为'GET '
# IPython
# In [0]: [ hex(ord(x)) for x in 'GET ']
# Out[0]: ['0x47', '0x45', '0x54', '0x20']
sudo tcpdump -X -s 0 -i en0 'tcp[(tcp[12]>>2):4] = 0x47455420'
```

## tree
```
# L:显示层数 I:忽略文件
tree -I '*.pyc|__*__|node_modules|bower_components' -L 3
```

## ssh

```
service ssh restart
```

## find

```
# 找出文件大小为1033文件
find . -name "*" -size +1033c

# 找到用户和群组归属的特定文件
find / -group bandit6 -user bandit7 -size 33c
```

## apt-cache

```
# 查看依赖
apt-cache depends "build-essential"
```

## echo

```
# 16 2 dec
echo $((16#7f))
```

## od

```
# 查看二进制文件
# -w8 每行显示8个字节
# -t x 2以16进制显示，每一列包含2个字节
# -A n 不显示偏移地址
# -v 显示重复'0'行，否则以'*'替代
cat main.o | od -w8 -t x2 -A n -v
```

## xxd

```
# 二进制查看文件
# -c 12每一行包含12个字节
# -g 4 每一列包含4个字节
xxd -g 4  -c 12 main.o
```

## printf

```
# 进制转换
printf '%d\n' 0xd
printf '%x\n' 11

# 16进制运算
printf '%x\n' $((0xdd-0x7f))
```

## hexdump

```
# -C 显示16进制和ASCII
hexdump -C test.o
```

## git

```
# 显示某一个版本的文件
git show HEAD^:db/tests/test_mysql.py
```

## apt-get install

```
# 安装指定版本
sudo apt-get install postgresql-common=151.pgdg12.4+1

```
