import os

PORT = 9000
DEBUG = True
# peewee
# BACKEND_MYSQL="mysql+pool://root:root@127.0.0.1/torweb?max_connections=20&stale_timeout=300"
mysql_port = os.getenv('DB_PORT_3306_TCP_PORT')
mysql_host = os.getenv('DB_PORT_3306_TCP_ADDR')

BACKEND_MYSQL = {
    'database': 'torweb',
    'max_connections': 20,
    'stale_timeout': 300,
    'user': 'root',
    'password': 'qwaszx',
    'host': mysql_host if mysql_host else '127.0.0.1',
    'port': int(mysql_port) if mysql_port else 3306
}
BACKEND_MONGO = "mongodb://127.0.0.1/torweb"
BACKEND_REDIS = ('localhost', 6379, 0)

COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"

log_path = '/var/tmp/'
avatar_upload_path = './static/images/avatars/'
default_avatar = "avatar_01.png"
default_page_limit = 3

sys_status = [0, 0, 0, 0]

domain = 'weixin.linevery.com'

