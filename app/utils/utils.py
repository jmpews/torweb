# coding:utf-8
import uuid

from custor.captcha import image_captcha

from settings.config import config
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result, login_required, random_str


class UploadImgHandler(BaseRequestHandler):
    @login_required
    def post(self, *args, **kwargs):
        img_name = str(uuid.uuid1())
        # import pdb;pdb.set_trace()
        file = self.request.files['imageFile'][0]
        img_name += file['filename']
        img_file = open(config.common_upload_path + img_name, 'wb')
        img_file.write(file['body'])
        print('Upload-File: '+img_name)
        self.write(json_result(0, {'image': img_name}))

class CaptchaHandler(BaseRequestHandler):
    def get(self, *args, **kwargs):
        captcha_str = random_str(4)
        captcha_data = image_captcha.generate(captcha_str)
        self.set_header("Content-type",  "image/png")
        # self.set_header('Content-length', len(image))
        self.set_cookie('captcha', captcha_str)
        self.write(captcha_data.getvalue())
