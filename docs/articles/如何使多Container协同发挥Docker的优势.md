Title: 如何使多Container协同发挥Docker的优势
Date: 2016-08-05 09:59
Author: jmpews
Category: docker
Tags: docker
Slug: mutiple-docker

这里用Docker部署一个torweb(Tornado, MySQL)服务作为例子. 将整个服务拆分为Web(Python)和MySQL放在不同的容器运行.

这里的torweb是我自己写的服务, https://github.com/jmpews/torweb , Dockerfile配置文件,  https://github.com/jmpews/dockerfiles


### 0x00 Web层部容器构建
几个注意点

1. 最好把需要完成一个任务的所有命令放在一行(`&&`), 因为docker使用行作为每一步的分割, 每执行一步就会做cache, 当出现错误, 下次执行会使用之前cache.
2. 注意基础依赖包的安装, 比如:`ssl`, `sqlite3`等
3. 需要将Dockerfile需要COPY的文件放到和Dockerfile同目录下.

Dockerfile文件如下:

```
FROM daocloud.io/library/ubuntu:14.04

MAINTAINER jmpews "jmpews@gmail.com"

# 将修改源所有命令放在一行用&&连接
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak \
&& sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
&& apt-get update

# DEBIAN_FRONTEND=noninteractive 不进行交互
# 先检查有没有安装 sqlite3 ssl
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
                                    build-essential \
                                    g++ \
                                    gcc \
                                    libc6-dev \
                                    make \
                                    python-pip \
                                    libssl-dev \
                                    openssl \
                                    sqlite3 \
                                    libsqlite3-dev \
    && apt-get install -y wget curl git
# 删除apt-get的缓存
# RUN rm -rf /var/lib/apt/lists/*

# 修改时区
RUN echo "Asia/Shanghai" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata

# COPY 目录下所有文件到指定目录下, 注意最后/保留
# 配置应用目录
RUN mkdir -p /app/torweb
COPY torweb /app/torweb/ #目标文件是目录拷贝目录下所有文件到指定目录下
COPY Python-3.5.2.tgz /root/ #拷贝指定文件到目录下

# Python环境配置, 修改为阿里源
RUN mkdir ~/.pip && echo '[global]\n\
index-url = http://mirrors.aliyun.com/pypi/simple/\n\
[install]\n\
trusted-host = mirrors.aliyun.com' > ~/.pip/pip.conf

# 配置Python3的环境
# RUN wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
RUN cd /root/ \
    && tar zxvf Python-3.5.2.tgz \
    && cd /root/Python-3.5.2 \
    && ./configure --prefix=/usr/local/python3.5.2 \
    && make && make install

# 使用virtualenv来做部署环境, 发现好像没啥用
# RUN pip install virtualenv \
#     && mkdir /virtualenv \
#     && cd /virtualenv \
#     && virtualenv -p /usr/local/python3.5.2/bin/python3 python3.5.2
# RUN . /virtualenv/python3.5.2/bin/activate \
#     && pip install -r requirements.txt

# 安装依赖torweb项目依赖
RUN cd /app/torweb \
    &&/usr/local/python3.5.2/bin/pip3 install -r requirements.txt

# 设置工作目录(默认目录)
WORKDIR /app/torweb

# EXPOSE默认不暴露端口, 只有加-P参数才会将该端口随机绑定一个宿主机可用端口
# EXPOSE 8888

# CMD相当于启动命令
CMD ["/usr/local/python3.5.2/bin/python3", "app.py"]

# EXPOSE 方式, 使用docker ps会发现绑定到宿主机随机可用端口
# docker run -d -P --link db:db jmpews/base:test1
# -p特定端口映射
# docker run -d -p 8888:8888 --link db:db jmpews/base:test1
```

### 0x01 MySQL容器构建
直接使用`daocloud.io/library/mysql:5.7.14`镜像.

启动MySQL作为一个容器.

```
# -e MYSQL_ROOT_PASSWORD 环境变量,启动Container必须设置的数据库密码
# --name 容器的名字
docker run --name torweb-mysql -e MYSQL_ROOT_PASSWORD=root -d daocloud.io/library/mysql:5.7.14
```

### 0x02 连接Web, MySQL两个容器
** 通过`--link`连接容器, 现在属于从属关系, 现在web层服务父容器可以通过隧道调用MySQL服务, MYSQL子容器通过注入环境变量来传递配置参数给torweb层父容器. **

通过`docker run -ti --link torweb-mysql:db jmpews/base:test1 /bin/bash -c env`, 可以发现注入了很多`DB_`的环境变量(`DB_`即为db别名的大写), 所以在程序中需要通过这些环境变量连接数据库.
![](http://oaxgrbqi8.bkt.clouddn.com/14703344757862.jpg)

刚才已经启动MySQL服务, 现在启动torweb服务

```
# torweb-mysql为容器name, db为容器别名
# 启动会执行Dockerfile里CMD对应的命令
docker run -d -p 8888:8888 --link torweb-mysql:db jmpews/base:test1
```

### 0x03 通过`Docker-Compose`更简洁快速部署
这样我们需要先启动MySQL服务, 再启动Web服务, 过程繁琐, Docker官方推荐使用`docker-compose`, 进行统一部署.

在目录下建立 `docker-compose.yml`, 然后使用 `docker-compose up` 配置.

具体配置目录如下.
![](http://oaxgrbqi8.bkt.clouddn.com/14703354062153.jpg)

具体配置文件内容如下.

```
# docker-compose.yml
torweb:
	# docker build目录
  build: ./web
  links:
    - db:db
  ports:
    - 8888:8888
  # 每次启动执行命令
  command: /usr/local/python3.5.2/bin/python3 app.py

db:
	# docker的基础镜像
  image: daocloud.io/library/mysql:5.7.14
  expose:
    - "3306"
  environment:
    MYSQL_ROOT_PASSWORD: root
```
