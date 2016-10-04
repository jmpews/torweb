#encoding: utf-8
from settings.common import *


log_path = '/var/tmp/'
BACKEND_MYSQL = {
    'database': 'torweb',
    'max_connections': 20,
    'stale_timeout': 300,
    'user': 'root',
    'password': 'qwaszx',
    'host': '127.0.0.1',
    'port': 3306
}
BACKEND_MONGO = "mongodb://127.0.0.1/torweb"
BACKEND_REDIS = ('localhost', 6379, 0)