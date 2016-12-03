Title: Open VPN搭建
Date: 2016-07-21 03:43
Author: jmpews
Category: linux
Tags: vpn
Slug: install-open-vpn

## 安装依赖
```
sudo yum update
sudo yum install openssl lzo pam pam-devel openssl-devel lzo-devel
sudo yum install easy-rsa
```

## 制作证书
```
cd /usr/share/easy-rsa/2.0/

vim ./vars
# 设置EY_COUNTRY, KEY_PROVINCE, KEY_CITY, KEY_ORG, and KEY_EMAIL几个参数
# These are the default values for fields
# which will be placed in the certificate.
# Don't leave any of these fields blank.
export KEY_COUNTRY="CN"
export KEY_PROVINCE="BJ"
export KEY_CITY="beijing"
export KEY_ORG="jmpews"
export KEY_EMAIL="jmpews@gmail.com"
export KEY_OU="jmpews"
# X509 Subject Field
export KEY_NAME="jmpewsvpn"

# 使vars生效, 生成证书
. ./vars
./clean-all
./build-ca

```

## 制作服务端证书
```
./build-key-server jmpewsvpn
```

## 制作客户端证书
```
./build-key client1
./build-key client2
./build-key client3
```

## 生成Hellman
```
./build-dh
```
## 剩下按照docs做即可

## 参考资料
---
https://openvpn.net/index.php/open-source/documentation/howto.html#install
