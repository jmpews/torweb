# conding:utf-8

from app.blog.blog import  (
    BlogIndexHandler,
    BlogPostDetailHandler,
    BlogPostOptHandler
)

urlprefix = r''

urlpattern = (
    (r'/blog', BlogIndexHandler),
    (r'/blog/(\d+)', BlogPostDetailHandler),
    (r'/blog/opt', BlogPostOptHandler),
)
