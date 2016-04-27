import sys, os
sys.path.append(os.path.dirname(sys.path[0]))
from backend.mysql_model import db_mysql
from backend.mysql_model.user import User
from backend.mysql_model.post import Post, PostReply

try:
    db_mysql.create_table(User)
except:
    print('User-表已经存在')


try:
    db_mysql.create_tables([Post, PostReply])
except:
    print('Post,PostReply-表已经存在')


def test_user():
    user=User.get_by_username('admin')
    if user:
        user.delete_instance()
        print('already exist <admin>,so delete it!')
    else:
        print('<admin> not exist')
    user=User.new(username='admin',nickname='admin',password='admin')
    print('new user <admin:admin>',user)

    user.set_password('root')
    print('change <admin> password to <root>')

    if User.auth('admin','admin'):
        print('auth success!')
    else:
        print('auth failed!')

    if User.exist('admin'):
        print('admin exist')
    else:
        print('admin not exist')
    print('User count ',User.count())

test_user()

def test_post():
    user=User.get_by_username('admin')
    post=Post.create(
        title="test_vul_scan",
        content="vul_scan_content_04.27_12:47",
        user=user
    )
    post.up_visit()
    post.up_collect()
    print('new post <test_vul_scan:admin>')
    postreply=PostReply.create(
        post=post,
        user=user,
        content='test_reply'
    )
    print('new postreply <test_reply:admin>')
    postreply.up_like()
    post.up_reply()

test_post()
