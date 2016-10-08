#coding: utf-8

from settings.common import *

PORT = 9001

BACKEND_MYSQL = {
    'database': 'torweb',
    'max_connections': 20,
    'stale_timeout': 300,
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'port': 3306
}
BACKEND_MONGO = "mongodb://127.0.0.1/torweb"
BACKEND_REDIS = ('localhost', 6379, 0)

STATIC_PATH = (
    (r'/static/(.*)', {'path': 'frontend/static/templates/static/'}),
    (r'/avatar/(.*)', {'path': 'frontend/static/assets/'}),
    (r'/assets/lib/(.*)', {'path': 'frontend/lib/'}),
    (r'/assets/(.*)', {'path': 'frontend/static/assets/'}),
    (r'/blog/images/(.*)', {'path': 'frontend/static/templates/blog/images/'}),
    (r'/dashboard/(.*)', {'path': 'frontend/static/templates/dashboard/'})
)

# docker-registry

TOKEN_EXPIRATION = 300
SERVICE = 'token-service'
ISSUER = 'registry-token-issuer'
private_key_path = './private_key.pem'