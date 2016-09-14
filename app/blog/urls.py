# conding:utf-8

from app.blog.blog import  (
    BlogIndexHandler,
    BlogPostDetailHandler
)

urlprefix = r''

urlpattern = (
    (r'/blog', BlogIndexHandler),
    (r'/blog/(\d+)', BlogPostDetailHandler),
)
