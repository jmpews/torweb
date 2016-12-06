# coding:utf-8
from db.mysql_model.post import CollectPost

def get_post_user_ext(post, user):
    ext = type('ext', (), {})
    is_collect = CollectPost.is_collect(post, user)
    if user:
        is_own = post.check_own(user)
        is_auth = user.is_admin()
    else:
        is_own = False
        is_auth = False

    setattr(ext, 'is_collect', is_collect)
    setattr(ext, 'is_own', is_own)
    setattr(ext, 'is_auth', is_auth)
    return ext

