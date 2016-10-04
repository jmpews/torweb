#!/usr/bin/env python
# coding: utf-8
import os

TEMPLATE_PATH = 'frontend/static/templates'
LOGIN_URL = '/login'
PORT = 9000
DEBUG = True
COOKIE_SECRET = "6aOO5ZC55LiN5pWj6ZW/5oGo77yM6Iqx5p+T5LiN6YCP5Lmh5oSB44CC"
sys_status = [0, 0, 0, 0]
# log_path = '/var/tmp/'
avatar_upload_path = './frontend/static/assets/images/avatar/'
common_upload_path = './frontend/static/assets/images/'
default_page_limit = 7
default_avatar = 'default_doubi.png'

static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
