# encoding:utf-8

import app.api.urls
import app.index.urls
import app.post.urls
import app.recommend.urls
import app.user.urls
import app.utils.urls

urlpattern = ()

urlpattern += app.api.urls.urlpattern
urlpattern += app.index.urls.urlpattern
urlpattern += app.post.urls.urlpattern
urlpattern += app.recommend.urls.urlpattern
urlpattern += app.user.urls.urlpattern
urlpattern += app.utils.urls.urlpattern


