import sys, os

sys.path.append(os.path.dirname(sys.path[0]))
from db.mysql_model import db_mysql
from db.mysql_model.user import User
from db.mysql_model.post import Post, PostReply

if User.table_exists():
    print('[User]表已经存在')
else:
    db_mysql.create_table(User)

if Post.table_exists():
    print('[Post]表已经存在')
else:
    db_mysql.create_table(Post)

if PostReply.table_exists():
    print('[PostReply]表已经存在')
else:
    db_mysql.create_table(PostReply)

PostReply.delete().execute()
Post.delete().execute()
User.delete().execute()


def test_user():
    user = User.get_by_username('admin')
    if user:
        user.delete_instance()
        print('already exist <admin>,so delete it!')
    else:
        print('<admin> not exist')
    user = User.new(username='admin', nickname='admin', password='admin')
    print('new user <admin:admin>', user)

    user.set_password('root')
    print('change <admin> password to <root>')

    if User.auth('admin', 'admin'):
        print('auth success!')
    else:
        print('auth failed!')

    if User.exist('admin'):
        print('admin exist')
    else:
        print('admin not exist')
    print('User count ', User.count())


test_user()


def test_post():
    user = User.get_by_username('admin')
    post = Post.create(
            title="test_vul_scan",
            content="vul_scan_content_04.27_12:47",
            user=user
    )
    post.up_visit()
    post.up_collect()
    print('new post <test_vul_scan:admin>')
    postreply = PostReply.create(
            post=post,
            user=user,
            content='test_reply'
    )
    print('new postreply <test_reply:admin>')
    postreply.up_like()
    post.up_reply()

    post_test = Post.create(
            title="IDS是一种积极主动的安全防护技术",
            content="入侵检测系统的核心价值在于通过对全网信息的分析，了解信息系统的安全状况，进而指导信息系统安全建设目标以及安全策略的确立和调整，而入侵防御系统的核心价值在于安全策略的实施—对黑客行为的阻击",
            user=user
    )
    postreply_test = PostReply.create(
            post=post,
            user=user,
            content='入侵检测系统需要部署在网络内部，监控范围可以覆盖整个子网，包括来自外部的数据以及内部终端之间传输的数据，入侵防御系统则必须部署在网络边界，抵御来自外部的入侵，对内部攻击行为无能为力。'
    )


test_post()
