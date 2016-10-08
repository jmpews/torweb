# jmp

## 关于Docker-Registry分支

docker分支是建立在[torweb-master](http://github.com/jmpews/torweb)之上的私有Registry.

主要是与现有的账户系统进行融合. 提供自定义授权的token-auth机制, 以及对Image的列表和检索.

关于Docker-Reigsty的搭建过程详见[docs/docker-registry-install.md](docs/docker-registry-install.md)

## 如何测试该私有Registry

由于暂时没有做https相关处理. 需要将该Registry设置为信任的Registry.

### OSX-Docker客户端
在 `Perferences... -> Advanced -> Insecure registryies` 添加 `110.110.10.149`

### Linux

> 1. Open the /etc/default/docker file or /etc/sysconfig/docker for editing.Depending on your operating system, your Engine daemon start options.
> 2. Edit (or add) the DOCKER_OPTS line and add the --insecure-registry flag.This flag takes the URL of your registry, for example. `DOCKER_OPTS="--insecure-registry myregistrydomain.com:5000"`
> 3. Close and save the configuration file.Restart your Docker daemon
> The command you use to restart the daemon depends on your operating system. For example, on Ubuntu, this is usually the service docker stop and service docker start command.

这里把 `DOCKER_OPTS="--insecure-registry myregistrydomain.com:5000"` 改为 `DOCKER_OPTS="--insecure-registry 110.110.10.149"` 进行上述操作

---

## torweb介绍

[torweb](http://github.com/jmpews/torweb)
