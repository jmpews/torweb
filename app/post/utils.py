#coding:utf-8
from db.mysql_model.post import CollectPost

def get_post_user_ext(post, user):
    ext = type('ext', (), {})
    is_collect = CollectPost.is_collect(post, user),
    is_own = post.check_own(user)
    setattr(ext, 'is_collect', is_collect)
    setattr(ext, 'is_own', is_own)
    return ext

