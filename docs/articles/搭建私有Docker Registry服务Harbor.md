Title: 使用Harbor搭建私有Docker Registry服务
Date: 2016-07-29 09:59
Author: jmpews
Category: docker
Tags: docker harbor
Slug: docker-harbor

docker提供registry的镜像但是没有比较完善的用户管理镜像管理的功能, harbor是vm开源的对于私有Registry解决方案.

## 安装
参考 https://github.com/vmware/harbor/blob/master/docs/installation_guide.md

harbar通过多个 `docker-compose` 管理多个container.

```
cd /harbor/Deploy
./prepare
```

这里有一种离线的方式install. 可以具体具体文档.

#### 1. 修改基础镜像源

替换所有docker hub的镜像为DaoCloud镜像, 例如:

```
# FROM mysql:5.6
FROM daocloud.io/library/mysql:5.6
```

#### 2. 修改镜像源
修改Dockerfile.ui,Dockerfile.job,添加源修改

```
+RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
+RUN echo "deb http://mirrors.163.com/debian/ jessie main non-free contrib" > /etc/apt/sources.list
+RUN echo "deb http://mirrors.163.com/debian/ jessie-updates main non-free contrib" >> /etc/apt/sources.list
+RUN echo "deb http://mirrors.163.com/debian/ jessie-backports main non-free contrib" >> /etc/apt/sources.list
+RUN echo "deb-src http://mirrors.163.com/debian/ jessie main non-free contrib" >> /etc/apt/sources.list
+RUN echo "deb-src http://mirrors.163.com/debian/ jessie-updates main non-free contrib" >> /etc/apt/sources.list
+RUN echo "deb-src http://mirrors.163.com/debian/ jessie-backports main non-free contrib" >> /etc/apt/sources.list
+RUN echo "deb http://mirrors.163.com/debian-security/ jessie/updates main non-free contrib" >> /etc/apt/sources.list
+RUN echo "deb-src http://mirrors.163.com/debian-security/ jessie/updates main non-free contrib" >> /etc/apt/sources.list
```

启动服务 `docker-compose up`

## 实践

```
# 登陆验证,增加insecure-registry选项
vim /etc/default/docekr
DOCKER_OPTS="$DOCKER_OPTS --insecure-registry=10.0.247.186"
service docker restart

# 登陆
docker login 10.0.247.186

# 上传镜像, 这里需要了解镜像的命名规则
docker tag daocloud.io/library/nginx:1.9 10.0.247.186/library/nginx:1.9
docker images
docker push 10.0.247.186/library/nginx:1.9
```
