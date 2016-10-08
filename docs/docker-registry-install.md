## 安装Docker-Registry

### 添加docker的中科大镜像源

在 `/etc/docker/daemon.json` 添加:

```
{
	"registry-mirrors": ["https://docker.mirrors.ustc.edu.cn"]
}
```

### 拉取registry

```
sudo docker pull registry:2.5
```

### 生成密钥和配置文件

```
git clone https://github.com/jmpews/dockerfiles

cd docker_registry

# 生成密钥和证书
openssl genrsa -out ./private_key.pem 4096
openssl req -new -x509 -key ./private_key.pem -out ./root.crt -days 3650 -subj /C=CN/ST=state/L=CN/O=jmp/OU=jmp\ unit/CN=jmpews.com/emailAddress=i@jmpews.com

# 载配置文件
cat registry.yaml

version: 0.1
log:
  level: debug
  fields:
    service: registry
storage:
    cache:
        layerinfo: inmemory
    filesystem:
        rootdirectory: /storage
    maintenance:
        uploadpurging:
            enabled: false
    delete:
        enabled: true
http:
    addr: :5000
    secret: placeholder
auth:
  token:
    issuer: registry-token-issuer
	# registry-auth-server地址
    realm: http://10.0.246.79:9000/registryauth/auth
    rootcertbundle: /etc/registry/root.crt
    service: token-service
```

### 启动registry

```
docker run -it --rm \
        -p 5000:5000 \
        -v `pwd`/root.crt:/etc/registry/root.crt:ro \
        -v `pwd`/registry.yaml:/etc/docker/registry/config.yml:ro \
		registry:2.5
```



