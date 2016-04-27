# coding:utf-8
import tornado.web
from backend.mysql_model.user import User
from backend.mysql_model.post import Post, PostReply
from handlers.basehandlers.basehandler import BaseRequestHandler

class PostDetailHandler(BaseRequestHandler):
    def get(self, post_id, *args, **kwargs):
        post=Post.get(Post.id==post_id)
        post_detail=post.detail()
        post_replys=PostReply.list_all(post)
        self.render('post_detail.html', post_detail=post_detail, post_replys=post_replys)
