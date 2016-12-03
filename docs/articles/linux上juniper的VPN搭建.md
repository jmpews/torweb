Title: Linux上Juniper的VPN搭建
Date: 2016-06-26 09:12
Author: jmpews
Category: linux
Tags: juniper,vpn
Slug: config-juniper-vpn
## Summary:

最近需要在自己的centos上搭建连接学校juniper-vpn跑一些内网服务。osx和win都可以使用Pulse Connect Secure。

需要使用`OpenConnect`搭建VPN。 http://www.infradead.org/openconnect


### Linux下搭建`OpenConnect`

```
# 安装依赖
yum install vpnc-script openssl-devel libxml2-devel
apt-get install vpnc-scripts libssl-dev libxml2-dev

# 安装openconnect
wget http://www.infradead.org/openconnect/download.html
tar xzvf openconnect-7.06.tar.gz
cd openconnect
./configure --with-vpnc-script=/etc/vpnc/vpnc-script --without-gnutls --without-openssl-version-check
make
make install

# 添加/usr/local/lib到环境变量到.bash_profile 或者 .bashrc
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

# 修改策略路由以允许其他服务正常被访问，否则会导致ssh等timeout
# x.x.x.x is your public IP, y.y.y.y/y is the subnet(IP:101.201.111.225 netmask:255.255.252.0 subnet:101.201.108.0/22), ethX is your public Ethernet interface, and z.z.z. is the default gateway(cat /etc/sysconfig/network)
ip rule add from x.x.x.x table 128
ip route add table 128 to y.y.y.y/y dev ethX #测试发现这一句即使没有也没事，因为ip route就没有关于to的option
ip route add table 128 default via z.z.z.z

# 开启VPN
openconnect --juniper --user=xxxx --no-cert-check https://sslvpn.xxx.edu.cn
openconnect --juniper --background --pid-file=/var/run/openconnect.pid --quiet --passwd-on-stdin --reconnect-timeout=30 --user=2012241004 --no-cert-check https://sslvpn.sxu.edu.cn
```
