# conding:utf-8

from app.post.post import (
    PostDetailHandler,
    PostAddHandler,
    PostReplyAddHandler,
    PostReplyOptHandler,
)

urlprefix = r''

urlpattern = (
    (r'/post/(\d+)', PostDetailHandler),
    (r'/post/add', PostAddHandler),
    (r'/postreply/add', PostReplyAddHandler),
    (r'/postreplyopt', PostReplyOptHandler),
)
