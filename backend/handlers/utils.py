# coding:utf-8
import tornado.web
import config
import uuid
from handlers.basehandlers.basehandler import BaseRequestHandler

from utils.util import json_result, login_required


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
