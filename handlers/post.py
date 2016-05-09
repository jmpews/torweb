# coding:utf-8
import tornado.web
from backend.mysql_model.user import User
from backend.mysql_model.post import Post, PostReply
from handlers.basehandlers.basehandler import BaseRequestHandler

from utils.util import login_required
from utils.util import get_cleaned_post_data


# 帖子详情
class PostDetailHandler(BaseRequestHandler):
    def get(self, post_id, *args, **kwargs):
        post=Post.get(Post.id==post_id)
        post_detail=post.detail()
        post_replys=PostReply.list_all(post)
        self.render('post_detail.html', post_detail=post_detail, post_replys=post_replys)

# 添加帖子
class PostAddHandler(BaseRequestHandler):
    @login_required
    def get(self, *args, **kwargs):
        self.render('post_new.html')

    @login_required
    def post(self, *args, **kwargs):
        post_data=get_cleaned_post_data(self,['title','content'])
        post=Post.create(
            title=post_data['title'],
            content=post_data['content'],
            user=self.current_user
        )
        self.redirect('/post/'+str(post.id))

