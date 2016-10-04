#coding: utf-8

from settings.common import *

log_path = '.'

PORT = 9001

SERVER_IP = '192.168.1.108'

BACKEND_MYSQL = {
    'database': 'tornadodemo',
    'max_connections': 20,
    'stale_timeout': 300,
    'user': 'tornado',
    'password': 'tornado',
    'host': '{0}'.format(SERVER_IP),
    'port': 3306
}
BACKEND_MONGO = "mongodb://{0}/torweb".format(SERVER_IP)
BACKEND_REDIS = ('{0}'.format(SERVER_IP), 6379, 0)

STATIC_PATH = (
    (r'/static/(.*)', {'path': 'frontend/static/templates/static/'}),
    (r'/avatar/(.*)', {'path': 'frontend/static/assets/'}),
    (r'/assets/lib/(.*)', {'path': 'frontend/lib/'}),
    (r'/assets/(.*)', {'path': 'frontend/static/assets/'}),
    (r'/blog/images/(.*)', {'path': 'frontend/static/templates/blog/images/'}),
    (r'/dashboard/(.*)', {'path': 'frontend/static/templates/dashboard/'})
)
