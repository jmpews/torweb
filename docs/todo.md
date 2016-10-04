## 完全安装

### 搭建python3环境
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

### 安装mysql等依赖服务

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

#### 安装nginx

```
sudo apt-get install nginx
vim /etc/nginx/conf.d/tornado.conf
upstream torweb {
	server 127.0.0.1:9001;
}
server {
	listen 9000;
    access_log  /usr/local/var/log/nginx/torweb.access.log;
    error_log  /usr/local/var/log/nginx/torweb.error.log;

	# Allow file uploads
    client_max_body_size 50M;

	location ^~ /assets/ {
	    root /Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static;
	    if ($query_string) {
	        expires max;
	    }
	}

	location ^~ /avatar/ {
	    root /Users/jmpews/Desktop/codesnippet/python/torweb/static/images;
	    if ($query_string) {
	        expires max;
	    }
	}

	location ^~ /dashboard/ {
	    root /Users/jmpews/Desktop/codesnippet/python/torweb/frontend/static/templates;
	    if ($query_string) {
	        expires max;
	    }
	}

	location = /favicon.ico {
		rewrite (.*) /static/favicon.ico;
	}
	location = /robots.txt {
		rewrite (.*) /static/robots.txt;
	}

	location / {
		proxy_http_version 1.1;
		proxy_read_timeout 300s;
		proxy_redirect off;
		proxy_pass_header Server;
		proxy_set_header Host $http_host;
		proxy_set_header Upgrade $http_upgrade;
		proxy_set_header Connection "upgrade";
		proxy_set_header X-Real-IP $remote_addr;
		proxy_set_header X-Scheme $scheme;
		proxy_pass http://torweb;
	}
}
```

### 启动服务

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
