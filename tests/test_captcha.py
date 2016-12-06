# coding:utf-8

import sys, os
import tornado.ioloop
from tornado import gen

sys.path.append(os.path.dirname(sys.path[0]))

from custor.captcha import image_captcha

data = image_captcha.generate('1234')
image_captcha.write('1234', 'out.png')
