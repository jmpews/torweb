# conding:utf-8

from app.user.user import (
    UserProfileHandler,
    UserProfileEditHandler,
    UserAvatarEditHandler,
    UserNotificationHandler,
    UserFollowerHandler,
    UserOptHandler,
    WebsocketChatHandler
)

urlprefix = r''

urlpattern = (
    (r'/user/(\d+)', UserProfileHandler),
    (r'/user/edit', UserProfileEditHandler),
    (r'/user/notification', UserNotificationHandler),
    (r'/user/chatwebsocket', WebsocketChatHandler),
    (r'/user/avatar/edit', UserAvatarEditHandler),
    (r'/useropt', UserOptHandler),
    (r'/follower/(\d+)', UserFollowerHandler),
)
