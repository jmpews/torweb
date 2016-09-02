# conding:utf-8

from app.utils.utils import (
    UploadImgHandler,
)

urlprefix = r''

urlpattern = (
    (r'/utils/uploadimg', UploadImgHandler),
)
