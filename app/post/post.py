# coding:utf-8
from app.cache import system_status_cache, hot_post_cache, topic_category_cache

from custor.handlers.basehandler import BaseRequestHandler
from custor.utils import get_cleaned_post_data, get_cleaned_json_data, json_result
from custor.decorators import login_required_json, login_required

from db.mysql_model.common import Notification
from db.mysql_model.post import Post, PostReply, PostTopic, CollectPost

from .utils import get_post_user_ext

import greenado
from settings.language import MSG


class PostDetailHandler(BaseRequestHandler):
    """
    post detail
    """
    @greenado.groutine
    def get(self, post_id, *args, **kwargs):
        post, post_replys = Post.get_detail_and_replys(post_id)
        if not post:
            self.redirect404()
            return
        ext = get_post_user_ext(post, self.current_user)
        self.render('post/post_detail.html',
                    post=post,
                    post_replys=post_replys,
                    ext=ext,
                    hot_post_cache=hot_post_cache,
                    topic_category_cache=topic_category_cache)


class PostAddHandler(BaseRequestHandler):
    """
    add post
    """
    @greenado.groutine
    @login_required
    def get(self, *args, **kwargs):
        self.render('post/post_new.html',
                    topic_category_cache=topic_category_cache)

    @greenado.groutine
    @login_required
    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['title', 'content', 'topic'])
        try:
            topic = PostTopic.get(PostTopic.str == post_data['topic'])
        except PostTopic.DoesNotExist:
            self.write(json_result(1, MSG.str()))
            return
        post = Post.create(
            topic=topic,
            title=post_data['title'],
            content=post_data['content'],
            user=self.current_user
        )
        # TODO: notification
        Notification.new_post(post)
        self.write(json_result(0, {'post_id': post.id}))


class PostModifyHandler(BaseRequestHandler):
    """
    modify post
    """
    @greenado.groutine
    @login_required
    def get(self, post_id, *args, **kwargs):
        post = Post.get_by_id(post_id)
        if not post.check_auth(self.current_user):
            self.redirect404()
            return
        self.render('post/post_modify.html',
                    post=post,
                    topic_category_cache=topic_category_cache)

    @greenado.groutine
    @login_required
    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['post', 'title', 'content', 'topic'])
        try:
            post = Post.get(Post.id == post_data['post'], Post.is_delete == False)
        except Post.DoesNotExist:
            self.write(json_result(1, '请选择正确主题'))
            return

        if not post.check_auth(self.current_user):
            self.redirect404_json()
            return

        try:
            topic = PostTopic.get(PostTopic.str == post_data['topic'])
        except PostTopic.DoesNotExist:
            self.write(json_result(1, '请选择正确主题'))
            return

        post.topic = topic
        post.title = post_data['title']
        post.content = post_data['content']
        post.save()

        # 添加通知, 通知给其他关注的用户
        Notification.new_post(post)
        self.write(json_result(0, {'post_id': post.id}))


class PostReplyAddHandler(BaseRequestHandler):
    @greenado.groutine
    @login_required
    def post(self, *args, **kwargs):
        post_data = get_cleaned_post_data(self, ['post', 'content'])
        try:
            post = Post.get(Post.id == post_data['post'], Post.is_delete == False)
        except PostTopic.DoesNotExist:
            self.write(json_result(1, '请选择正确post'))
            return
        postreply = PostReply.create(
            post=post,
            user=self.current_user,
            content=post_data['content'],
        )
        post.update_latest_reply(postreply)
        Notification.new_reply(postreply, post)
        self.write(json_result(0, {'post_id': post.id}))


# 帖子相关操作, 类似API的方式, 需要有opt,data参数(统一格式)
class PostReplyOptHandler(BaseRequestHandler):
    """
    A set of operation of
    """
    @greenado.groutine
    @login_required_json(-3, 'login failed.')  # 要求登录, 否则返回(错误码, 错误信息)
    def post(self, *args, **kwargs):
        json_data = get_cleaned_json_data(self, ['opt', 'data'])
        data = json_data['data']
        opt = json_data['opt']
        # 支持某个回复
        if opt == 'support-postreply':
            try:
                postreply = PostReply.get(PostReply.id == data['postreply'])
            except:
                self.write(json_result(1, '请输入正确的回复'))
                return
            postreply.up_like()
            self.write(json_result(0, 'success'))
        # 收藏该主题
        elif opt == 'collect-post':
            try:
                post = Post.get(Post.id == data['post'], Post.is_delete == False)
            except:
                self.write(json_result(1, '请输入正确的Post'))
                return
            CollectPost.create(post=post, user=self.current_user)
            self.write(json_result(0, 'success'))
        # 取消收藏该主题
        elif opt == 'cancle-collect-post':
            try:
                post = Post.get(Post.id == data['post'], Post.is_delete == False)
            except:
                self.write(json_result(1, 'CollectPost不正确'))
                return
            collectpost = CollectPost.get(post=post, user=self.current_user)
            collectpost.delete_instance()
            self.write(json_result(0, 'success'))
        # 取消收藏该主题
        elif opt == 'del-post':
            try:
                post = Post.get(Post.id == data['post-id'], Post.is_delete == False)
            except:
                self.write(json_result(1, 'CollectPost不正确'))
                return
            if not post.check_auth(self.current_user):
                self.redirect404_json()
                return
            post.logic_delete()
            self.write(json_result(0, 'success'))
        else:
            self.write(json_result(1, 'opt不支持'))
