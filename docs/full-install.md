## 搭建python3环境

```
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
tar zxvf Python-3.5.2.tgz
./configure --prefix=/usr/local/python3.5.2
make & make install
# 使用virtualenv创建隔离环境
pip install virtualenv
mkidr ~/virtualenv
virtualenv -p /usr/local/python3.5.2/bin/python3.5
```

---

## 安装mysql等依赖服务

#### 安装mysql

```
#!/usr/bin/env bash

# This is assumed to be run as root or with sudo

export DEBIAN_FRONTEND=noninteractive

# Import MySQL 5.7 Key
# gpg: key 5072E1F5: public key "MySQL Release Engineering <mysql-build@oss.oracle.com>" imported
apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys 5072E1F5
echo "deb http://repo.mysql.com/apt/ubuntu/ trusty mysql-5.7" | tee -a /etc/apt/sources.list.d/mysql.list

apt-get update

# Install MySQL

MYSQL_PASS="qwaszx"

debconf-set-selections <<< "mysql-community-server mysql-community-server/data-dir select ''"
debconf-set-selections <<< "mysql-community-server mysql-community-server/root-pass password $MYSQL_PASS"
debconf-set-selections <<< "mysql-community-server mysql-community-server/re-root-pass password $MYSQL_PASS"
apt-get install -y mysql-server
```

#### 安装Mongo

参考: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-linux/

```
curl -O https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.4.tgz
tar -zxvf mongodb-linux-x86_64-3.4.tgz
mkdir -p mongodb
cp -R -n mongodb-linux-x86_64-3.4/ mongodb
export PATH=<mongodb-install-directory>/bin:$PATH
```

#### 安装nginx

`tornado.conf` 请参考 [configs/nginx/tornado.conf](configs/nginx/tornado.conf)

---

## 启动服务

```
# py3环境
source ~/virtualenv/python3.5.2/bin/active
git pull https://github.com/jmpews/torweb.git
# 依赖包
pip install -r requirements.txt
# 修改配置文件
vim settings/develoment.py
# 导入测试数据
python tests/test_mysql.py
# 启动服务
python app.py
```
