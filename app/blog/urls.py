# conding:utf-8

from app.blog.blog import  (
    BlogIndexHandler,
    BlogPostDetailHandler,
    BlogPostOptHandler,
    BlogIndexCategoryHandler,
    BlogIndexLabelHandler
)

urlprefix = r''

urlpattern = (
    (r'/blog', BlogIndexHandler),
    (r'/blog/post/(\d+)', BlogPostDetailHandler),
    (r'/blog/opt', BlogPostOptHandler),
    (r'/blog/category/(\S+)', BlogIndexCategoryHandler),
    (r'/blog/label/(\S+)', BlogIndexLabelHandler),
)
