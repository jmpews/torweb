Title: SYNcookie原理
Date: 2016-10-19 03:43
Author: jmpews
Category: 协议栈
Tags: syn
Slug: syncookie

在研究syncookie的时候首先需要明确需要搞清的问题.

1. syncookie是为了解决什么问题? 

2. syncookie是怎么解决的? 

### syncookie解决了什么问题?

SYN flood(SYN洪水攻击, 不断发送伪造的SYN给服务器), 导致服务器上**半连接队列满**, 丢弃之后正常请求的SYN.

### syncookie 是怎么解决的?

#### 正常的过程, 半连接队列未满
1. 服务前端接收到 SYN(seq_a), 判断队列有没有如果没有满, 按照正常的处理过程, 将 SYN 放到半连接队列中, 回应SYN(seq_b)+ACK(seq_a+1)
2. 客户端回应ACK(seq_b+1), 服务端接受到客户端 ACK, 去检查半连接队列里是否有对应的 SYN, 如果有建立连接, 放到连接完成队列

#### SYN foold攻击, 半连接队列满
1. 接收到 SYN, 判断半连接队列是否满, 是否开启了syncookie, 按照syncookie进行接下来处理

2. 将接收到的 SYN 进行算法hash, 将关键的字段加密成 **服务端回应的SYN的seq** , 发送给客户端ACK+SYN(此时seq=hash后的而关键数值), 并丢弃SYN. (可以类比seq为base64-encode过程)

3. 如果客户端是正常的客户端会对服务器端的SYN(seq)回应ACK(seq+1)

4. 服务端接收到 ACK(seq+1), 先检查半连接队列是否存在该ACK对应的SYN, 如果不存在, 继续检查是否开启了syncookie, 如果开启了, 就检查seq是否为合法cookie, 如果是则对其进行逆运算, 恢复之前SYN, 继续操作.(可以类比base64-decode)

### 参考资料

http://blog.csdn.net/justlinux2010/article/details/12619761

[Syncookie源码解析（linux-2.6.30.10](http://m.blog.chinaunix.net/uid-23207633-id-267571.html)
