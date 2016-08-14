# coding:utf-8
import tornado.web
from backend.mysql_model.post import Post, PostReply, PostTopic
from handlers.basehandlers.basehandler import BaseRequestHandler
from handlers.cache import catetopic


from utils.util import login_required, json_result
from utils.util import get_cleaned_post_data



# 帖子详情
class PostDetailHandler(BaseRequestHandler):
    def get(self, post_id, *args, **kwargs):
        post = Post.get(Post.id == post_id)
        post.up_visit()
        post_detail = post.detail()
        post_replys = PostReply.list_all(post)
        self.render('post_detail.html', post_detail=post_detail, post_replys=post_replys)


# 添加帖子
class PostAddHandler(BaseRequestHandler):
    @login_required
    def get(self, *args, **kwargs):
        self.render('post_new.html',
                    catetopic=catetopic)

    @login_required
    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['title', 'content', 'topic'])
        try:
            topic = PostTopic.get(PostTopic.str == post_data['topic'])
        except PostTopic.DoesNotExist:
            self.write(json_result(1, '请选择正确主题'))
            return
        post = Post.create(
            topic=topic,
            title=post_data['title'],
            content=post_data['content'],
            user=self.current_user
        )
        self.write(json_result(0, {'post_id': post.id}))
