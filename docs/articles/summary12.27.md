Title: summary-12-27
Date: 2016-2-27 03:43
Author: jmpews
Category: 未分类
Tags: proxy
Slug: summary-12-27

Watch and Learn,Learn and Think.

最近一直在做两个东西:mini-httpdserver 和代理扫描自动代理的工具

先说说mini-httpdserver:

用pure c写的一个Httpserver，提供简单的web访问，对request和response进行分模块处理，并且提供了简单的路由。而且把我把很多资料放到该目录下，只要`git clone`就可以提供服务。

重点下代理扫描和自动代理:

在这个过程中走了很多弯路，原本以为通过select和epoll进行非阻塞的connect，并且手动做好timeout设置，每秒并发会上万已经是很快了。但是最近了解到Zmap，只要一听到它是通过**发送SYN半连接**来判断就明白了好多，只进行三次握手的第一步，整个过程不建立连接,因为自己写过一个用python发送原生TCP、IP、以太网包的程序，同时也可以监听本地数据包。Zmap就是不断发送SYN包，通过接受目标主机的ACK包，进行判断端口有没有开放，先缩小结果，然后进行connect发送验证数据包.

上面是扫描代理遇到坑，关于自动代理，之前想做的是，扫描代理形成一个自己的代理IP库，然后打算实现自动代理。

先说下客户端的自动代理：

在python上给socket打上patch，一开始是把patch打到connect上，重新实现connect，然后的做法是用装饰器去包装connect，第二种更简单一些。但是发现自己用用还可以，但是很难写成接口。connect之前get一个proxy，connect连接到proxy，然后发送请求，get这个从哪里获取。其实和人家request又有什么区别呢？从列表中get一个proxy，设置到request上，开一个线程，反正，鸡肋。

另一种做法就建立一个本地代理，程序中只需要设置好本地代理就ok，本地代理负责挑选代理进行转发。

