PORT = 9000
DEBUG = True

# peewee
# BACKEND_MYSQL="mysql+pool://root:root@127.0.0.1/torweb?max_connections=20&stale_timeout=300"
BACKEND_MYSQL={
    'database':'torweb',
    'max_connections':20,
    'stale_timeout':300,
    'user':'root',
    'password':'toor',
}
BACKEND_MONGO= "mongodb://127.0.0.1/torweb"
BACKEND_REDIS=('localhost',6379,0)

COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"

log_path='./'

domain='weixin.linevery.com'

