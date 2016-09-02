# conding:utf-8

from app.recommend.recommend import (
    RecommendHandler,
)

urlprefix = r''

urlpattern = (
    (r'/recommend', RecommendHandler),
)
