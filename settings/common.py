# coding:utf-8
import os

# Server
PORT = 9000
DEBUG = True

# log file
log_path = '/var/tmp/'

# cache
sys_status = [0, 0, 0, 0]

# Tornado
COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"
TEMPLATE_PATH = 'frontend/templates'
LOGIN_URL = '/login'
avatar_upload_path = './frontend/static/assets/images/avatar/'
common_upload_path = './frontend/static/assets/images/'
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
default_page_limit = 7
default_avatar = 'default_doubi.png'
default_404_url = '/static/404.html'

