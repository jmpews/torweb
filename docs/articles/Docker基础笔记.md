Title: Docker基础笔记
Date: 2016-07-14 09:59
Author: jmpews
Category: docker
Tags: docker
Slug: study-docker

**文档地址 `https://docs.docker.com`**

比较不错的入门实践 `https://www.gitbook.com/book/yeasy/docker_practice`

个人Dockerfile集合 `https://github.com/jmpews/dockerfiles`

必备命令 `docker --help`

## 0x0. docker 架构
---

Docker采取的C-S结构。Docker client同Docker daemon通讯，Docker daemon负责维护docker 容器的构建，运行和分发。
Client和Daemon可以再同一台主机上面执行，也可以分开执行。本地的client可以连接远程的daemon。Client可以通过socker或者REST API同daemon通讯。
![docker-architecture](https://docs.docker.com/engine/article-img/architecture.svg)

## 0x1. images 和 container 的关系
---

container建立在images之上, images有多种获取方式，`daocloud.io` / `https://c.163.com/`, 建议首选`daocloud.io`;当通过images运行命令自动就生成一个container,例如: `docker run -ti jmpews/go1.6 /bin/bash`

## 0x2. docker 基本配置信息
---

docker版本信息 `docker version`

docker配置信息 `docker info`

docker image(jmpews/go1.6)的配置信息 `docker inspect jmpews/go1.6`

docker存放images的位置(OSX) `~/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/Docker.qcow2`

## 0x3. Dockerfile实例
---

使用daocloud.io/library/ubuntu:14.04作为基础image构建自己的image

```
FROM daocloud.io/library/ubuntu:16.04

MAINTAINER jmpews "jmpews@gmail.com"

# 修改源
RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak \
&& sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
&& apt-get update

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
build-essential \
gdb \
python \
python-pip \
vim \
curl \
wget \
git \
tmux

# 修改时区
RUN echo "Asia/Shanghai" > /etc/timezone && dpkg-reconfigure -f noninteractive tzdata
# tmux配置文件
RUN wget --no-check-certificate -qO $HOME/.tmux.conf https://raw.githubusercontent.com/jmpews/configs/master/tmux/.tmux.conf
RUN tmux start-server
# vim配置文件
RUN wget --no-check-certificate -qO $HOME/.vimrc https://raw.githubusercontent.com/jmpews/configs/master/vim/.vimrc

# # Python环境配置
# RUN mkdir ~/.pip && echo '[global]\n\
# index-url = http://mirrors.aliyun.com/pypi/simple/\n\
# [install]\n\
# trusted-host = mirrors.aliyun.com' > ~/.pip/pip.conf

# # RUN wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
# RUN cd /root/ \
# 	&& wget --no-check-certificate -qO ./Python-3.5.2.tgz https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz \
#     && tar zxvf Python-3.5.2.tgz \
#     && cd /root/Python-3.5.2 \
#     && ./configure --prefix=/usr/local/python3.5.2 \
#     && make && make install

# Peda 安装
RUN GIT_SSL_NO_VERIFY=true git clone https://github.com/longld/peda.git ~/peda \
	&& echo "source ~/peda/peda.py" >> ~/.gdbinit \
	&& echo "DONE! debug your program with gdb and enjoy"
WORKDIR /root
```
## 0x4. Docker命令集合
---
### 0x01. `EXPOSE`和`-p`区别

```
# 默认不会进行映射，当使用`-P`会自动选择一个主机的端口映射好
EXPOSE 1000
# 指定docker和宿主机的特定端口映射
-p 5000:5000
```
