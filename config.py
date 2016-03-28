# coding:utf-8

PORT = 9000
DEBUG = True
APP_NAME = 'sxuhelp'
TITLE = 'sxuhelp'
TEMPLATE = 'tornado'  # jinja2/mako/tornado

Enable_Url_Count=True

# BACKEND_MYSQL="mysql+pymysql://root:root@192.168.33.10/sxuhelp"
# BACKEND_MONGO= "mongodb://192.168.33.10/sxuhelp"

#peewee
BACKEND_MYSQL="mysql+pool://root:root@127.0.0.1/tornado?max_connections=20&stale_timeout=300"
BACKEND_MONGO= "mongodb://127.0.0.1/tornado"
BACKEND_REDIS=('localhost',6379,0)

# BACKEND_MYSQL="mysql+pymysql://root:root@10.0.250.61/sxuhelp"
# BACKEND_MONGO= "mongodb://10.0.250.61/sxuhelp"

COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"

domain='weixin2.linevery.com'

