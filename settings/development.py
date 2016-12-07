# coding:utf-8

from settings.common import *

PORT = 9001


# BACKEND_REDIS = ('localhost', 6379, 0)

# Mongo Database
BACKEND_MONGO = {
    'host': 'localhost',
    'port': 27017

}
# MySQL Database
BACKEND_MYSQL = {
    'database': 'torweb',
    'max_connections': 20,
    'stale_timeout': 300,
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306
}

# Static Path
STATIC_PATH = (
    (r'/static/(.*)', {'path': 'frontend/templates/static/'}),
    (r'/assets/(.*)', {'path': 'frontend/static/assets/'}),
    (r'/dashboard/(.*)', {'path': 'frontend/templates/dashboard/'})
)