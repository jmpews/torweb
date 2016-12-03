Title: 搭建docker-registry的开发环境(在非docker镜像下跑registry服务)
Date: 2016-11-02 09:59
Author: jmpews
Category: docker
Tags: docker, registry, distribution
Slug: dev-docker-registry-distribution

因为最近需要搭建私有的docker-registry, 官方建议使用 `registry:2.5` 镜像搭建私有registry, 但是这需要在服务器跑docker, 打算直接跑 `distribution` 应用.

## 具体实践

```
# 也可以wget最近的release版本
git pull https://github.com/docker/distribution.git

# 把源码放到$GOPATH/src/github.com/下 因为registry中引用包都是'github.com/distribution/*'
mv distribution $GOPATH/src/github.com/

# 生成版本信息
cd distribution/version/
./version.sh>>version.go

# 编译registry
cd distribution/cmd/registry/
go build

# 设置存储位置, 运行registry服务
export REGISTRY_STORAGE_FILESYSTEM_ROOTDIRECTORY=/somewhere
./registry --version

./registry serve ./config-example.yml
```

## 参考文档

distribution的dockerfile :
> https://github.com/docker/distribution/blob/master/Dockerfile

distribution的dev开发环境搭建 :
> https://github.com/docker/distribution/blob/master/BUILDING.md
