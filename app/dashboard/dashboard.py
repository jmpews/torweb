#coding:utf-8
from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import json_result, get_cleaned_post_data, get_cleaned_query_data, get_page_number, get_page_nav, get_cleaned_json_data

from settings.config import config

from db.mysql_model.post import Post, PostTopic
from db.mysql_model.user import User
class IndexHandler(BaseRequestHandler):
    """
    后台面板首页
    """
    def get(self, *args, **kwargs):
        self.render('dashboard/pages/db-post-list.html')