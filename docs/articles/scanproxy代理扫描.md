Title: ScanProxy代理扫描(旧)
Date: 2015-11-03 01:21
Author: jmpews
Category: python
Tags: 代理扫描
Slug: scan-proxy

## 简介
分析协议构造验证数据，采用异步非阻塞socket发送数据，不采用request的方式。后记来到公司，发现用Zmap来说进行一遍预扫，然后再精确扫，这样会更快,而且使用go的协程来做.

## 更新!!!!!!!!：
---
先用Zmap进行全网扫一段，因为Zmap扫描是半连接，组成SYN包发送，组成包的发送不经过内核管理，发送SYN包，目标主机返回ACK包，但host收到ACK包，但是host不明确(因为之前就没有进过内核)，所以对外发送RST包，通过Zmap的原理可以查看，这样经过几个小时的全局扫描，对开放的端口进行具体的connect发送代理验证字符串

---

采用非阻塞的connect,每个IP测试4个端口。

之前没分清国内和国外的IP段，导致去扫国外的，一片超时。所以才有下文的超时处理，但是国内一般不会涉及到超时。但这里还是要说下自己的想法。

首先采用非阻塞的connect，会立即返回，如果返回`EINPROGRESS`,表明正在连接属于正常，在此期间使用`getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)`获取socket的错误，无论对于*正在连接*还是*连接完成*都返回0,直到出现超时异常或其他错误，才返回其他错误码。

##### 如果我们提前做超时异常处理，如何做？
假如三次握手包，要在网络中存在N秒多，那这几秒内，没有函数去判断是否连接完成，因为处在正在连接的过程中，`getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)`对于*正在连接*和*连接完成*的socket都返回0。但是我们可以通过`read()`或者`send()`或者`getpeername()`报异常，来判断。

几个注意点:

* 1.IP的区段 http://ips.chacuo.net/
* 2.非阻塞connect的返回码'EINPROGRESS',表示正在连接
* 3.http代理的验证方式,send一段http报文,验证返回.

## Http代理
当你发送`CONNECT %s:%s HTTP/1.1\r\nHost: %s:%s\r\nProxy-Connection: keep-alive\r\n\r\n`,接收到的response包含`b'Connection established'`表明，可以作为代理

## Socks5代理
当你发送`b'\x05\x02\x00\x02'`，接收到的data包含`b'\x05\x00'`,可以作为代理，这里仅仅是简单说明，但其中还涉及到验证等等复杂问题。

##### proxys.py
```
__author__ = 'jmpews'
import socket
from redisq import RedisQueue
import errno
import select
import time
import utils

# 采用非阻塞的connect,每个IP测试4个端口,手动做好每个socket的connect的超时处理
# 几个注意点:
# 1.IP的区段 http://ips.chacuo.net/
# 2.非阻塞connect的返回码'EINPROGRESS',表示正在连接
# 3.http代理的验证方式,send一段http报文,验证返回.


rq=RedisQueue('proxy')

ipfile=open('ip_shanghai.txt','r',encoding='utf-8')
iplist=[]
for line in ipfile:
    tmp=line.split('\t')
    iplist.append((tmp[0],tmp[1]))

ips=utils.genips(iplist)
# ips=utils.genips([('40.3.125.51','70.0.0.128')])
inputs=[]
outputs=[]
outputimeouts=[]

#test
# outputimeouts+=utils.addips('118.144.108.254')

while True:

    # 清除超时connect
    # 由于非阻塞的connect,所以要手动排除超时的connect
    outputimeouts=list(filter(utils.checktimeout,outputimeouts))

    # 维持数据数量
    if len(outputimeouts)<400:
        for i in range(100-int(len(outputimeouts)/4)):
            try:
                ip=ips.__next__()
            except StopIteration:
                # 循环到ip列表最后
                break
            outputimeouts+=utils.addips(ip)

    #补充数据
    outputs=[x[0] for x in outputimeouts]

    readable,writeable,exceptional=select.select(inputs,outputs,[],4)
    for x in readable:
        try:
            data=x.recv(1024)
            print(data)
        except Exception as e:
            x.close()
            print(e)
        if utils.checkhttp(data):
            detial=x.getpeername()
            print(detial)
            rq.put(detial[0]+':'+str(detial[1]))
        inputs.remove(x)
        x.close()

    for x in writeable:
        erro=x.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        # connect拒绝
        if erro==errno.ECONNREFUSED:
            # print('conn refuse.')
            outputimeouts=list(filter(lambda tm:tm[1]!=x.fileno(),outputimeouts))
            # outputs.remove(x)
            x.close()
            continue

        # 超时
        elif erro==errno.ETIMEDOUT:
            # print('conn timeout.')
            outputimeouts=list(filter(lambda tm:tm[1]!=x.fileno(),outputimeouts))
            # outputs.remove(x)
            x.close()
            continue

        # 不可到达
        elif erro==errno.EHOSTUNREACH:
            # print('host unreach.')
            outputimeouts=list(filter(lambda tm:tm[1]!=x.fileno(),outputimeouts))
            # outputs.remove(x)
            x.close()
            continue

        # 正常connect
        # 发送http代理验证数据
        elif erro==0:
            print('connect success')
            utils.sendhttp(x)
            outputimeouts=list(filter(lambda tm:tm[1]!=x.fileno(),outputimeouts))
            # outputs.remove(x)
            inputs.append(x)

    for x in exceptional:
        print('====EXCEP====')

    # ip=ips.__next__()
    # print(ip)
    # print('loop...')
```

##### utils.py
```
__author__ = 'jmpews'
import socket
import time

#发送验证字符串
def sendhttp(x):
    t=x.getpeername()
    connstr="CONNECT %s:%s HTTP/1.1\r\nHost: %s:%s\r\nProxy-Connection: keep-alive\r\n\r\n" % (t[0],t[1],t[0],t[1])
    x.send(connstr.encode())

#检查response是否存在字符串
def checkhttp(data):
    if data.find(b'Connection established')==-1:
        return False
    return True

# 发送socks验证数据
def sendsocks(x):
    x.send(b'\x05\x02\x00\x02')

#检查response是否存在字符串.
def checksocks(data):
    if data.find(b'\x05\x00') == -1:
        return False
    return True

# 采用生成器方式,防止超长list爆内存
def genips(ipl):
    def s2n(str):
        i=[int(x) for x in str.split('.')]
        return i[0]<<24|i[1]<<16|i[2]<<8|i[3]
    def n2ip(num):
        return '%s.%s.%s.%s' % (
            (num&0xFF000000)>>24,
            (num&0x00FF0000)>>16,
            (num&0x0000FF00)>>8,
            (num&0x000000FF)
        )
    for s,e in ipl:
        for t in range(s2n(s),s2n(e)):
            yield n2ip(t)


# 对于每个IP生成4个socket,表示检查4个常见端口
def addips(ip):
    httports=[80,3128,8080,8888]
    socks=[]
    tm=int(time.time())
    for port in httports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 非阻塞connect
        sock.setblocking(0)
        err=sock.connect_ex((ip, port))
        socks.append((sock,sock.fileno(),tm))
    return socks

# 检查sock是否超时
def checktimeout(x):
    t=time.time()
    if x[2]+3<t:
        try:
            x[0].getpeername()
        except:
            # print('Exp:Host.')
            x[0].close()
            return False
    return True
```
