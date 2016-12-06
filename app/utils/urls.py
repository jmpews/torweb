# coding:utf-8

from app.utils.utils import (
    UploadImgHandler,
    CaptchaHandler
)

urlprefix = r''

urlpattern = (
    (r'/utils/uploadimg', UploadImgHandler),
    (r'/utils/captcha', CaptchaHandler),
)
