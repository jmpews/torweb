Title: IPSec VPN搭建
Date: 2016-2-27 03:43
Author: jmpews
Category: linux
Tags: vpn
Slug: setup-ipsec-vpn

## 安装依赖
```
yum update
yum install pam-devel openssl-devel make gcc
```

## 安装strongswan
```
yum -y install strongswan (strongswan-libipsec,openvz架构需要)
```

## 生成CA证书

```
strongswan pki --gen --outform pem > caKey.pem
strongswan pki --self --in caKey.pem --dn "C=CN, O=strongSwan, CN=strongSwan CA" --ca --outform pem > caCert.pem
```

## 生成Server端证书

```
strongswan pki --gen --outform pem > serverKey.pem
strongswan pki --pub --in serverKey.pem | strongswan pki --issue --cacert caCert.pem --cakey caKey.pem --dn "C=CN, O=strongSwan, CN=45.32.47.162" --san="45.32.47.162" --flag serverAuth --flag ikeIntermediate --outform pem > serverCert.pem
```

## 生成Client端证书
```
strongswan pki --gen --outform pem > clientKey.pem
strongswan pki --pub --in clientKey.pem | strongswan pki --issue --cacert caCert.pem --cakey caKey.pem --dn "C=CN, O=strongSwan, CN=client" --outform pem > clientCert.pem
```

## Client证书转换为.p12格式
```
openssl pkcs12 -export -inkey clientKey.pem -in clientCert.pem -name "client" -certfile caCert.pem -caname "strongSwan CA" -out clientCert.p12
```

## 安装证书

```
mv -f caCert.pem /etc/strongswan/ipsec.d/cacerts/
mv -f serverCert.pem /etc/strongswan/ipsec.d/certs/
mv -f serverKey.pem /etc/strongswan/ipsec.d/private/
mv -f clientCert.pem /etc/strongswan/ipsec.d/certs/
mv -f clientKey.pem /etc/strongswan/ipsec.d/private/
```

## 配置Strongswan
```
bash -c "cat > /etc/strongswan/ipsec.conf<<EOF
config setup
    uniqueids=never
conn iOS_cert
    keyexchange=ikev1
    # strongswan version >= 5.0.2, compatible with iOS 6.0,6.0.1
    fragmentation=yes
    left=%defaultroute
    leftauth=pubkey
    leftsubnet=0.0.0.0/0
    leftcert=server.cert.pem
    right=%any
    rightauth=pubkey
    rightauth2=xauth
    rightsourceip=10.31.2.0/24
    rightcert=client.cert.pem
    auto=add
conn android_xauth_psk
    keyexchange=ikev1
    left=%defaultroute
    leftauth=psk
    leftsubnet=0.0.0.0/0
    right=%any
    rightauth=psk
    rightauth2=xauth
    rightsourceip=10.31.2.0/24
    auto=add
conn networkmanager-strongswan
    keyexchange=ikev2
    left=%defaultroute
    leftauth=pubkey
    leftsubnet=0.0.0.0/0
    leftcert=server.cert.pem
    right=%any
    rightauth=pubkey
    rightsourceip=10.31.2.0/24
    rightcert=client.cert.pem
    auto=add
conn windows7
    keyexchange=ikev2
    ike=aes256-sha1-modp1024!
    rekey=no
    left=%defaultroute
    leftauth=pubkey
    leftsubnet=0.0.0.0/0
    leftcert=server.cert.pem
    right=%any
    rightauth=eap-mschapv2
    rightsourceip=10.31.2.0/24
    rightsendcert=never
    eap_identity=%any
    auto=add
EOF"
```

## 配置Strongswan的配置文件

```
bash -c "cat > /etc/strongswan/strongswan.conf<<EOF
 charon {
         load_modular = yes
         duplicheck.enable = no
         compress = yes
         plugins {
                 include strongswan.d/charon/*.conf
         }
         dns1 = 8.8.8.8
         dns2 = 8.8.4.4
         nbns1 = 8.8.8.8
         nbns2 = 8.8.4.4
 }
 include strongswan.d/*.conf
EOF"
```

## 设置认证方式

```
bash -c "cat > /etc/strongswan/ipsec.secrets<<EOF
: RSA server.pem
: PSK \"seckey\"
: XAUTH \"seckey\"
nyt %any : EAP \"hello\"
jmpews %any : EAP \"hello\"
EOF"
```

## 调整IPTABLES

```
iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -s 10.31.0.0/24  -j ACCEPT
iptables -A FORWARD -s 10.31.1.0/24  -j ACCEPT
iptables -A FORWARD -s 10.31.2.0/24  -j ACCEPT
iptables -A INPUT -i eth0 -p esp -j ACCEPT
iptables -A INPUT -i eth0 -p udp --dport 500 -j ACCEPT
iptables -A INPUT -i eth0 -p tcp --dport 500 -j ACCEPT
iptables -A INPUT -i eth0 -p udp --dport 4500 -j ACCEPT
iptables -A INPUT -i eth0 -p udp --dport 1701 -j ACCEPT
iptables -A INPUT -i eth0 -p tcp --dport 1723 -j ACCEPT
iptables -A FORWARD -j REJECT
iptables -t nat -A POSTROUTING -s 10.31.0.0/24 -o eth0 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 10.31.1.0/24 -o eth0 -j MASQUERADE
iptables -t nat -A POSTROUTING -s 10.31.2.0/24 -o eth0 -j MASQUERADE
```
