from config import BACKEND_MYSQL
from peewee import Model, MySQLDatabase
from playhouse.pool import PooledMySQLDatabase

# PooledMySQLDatabase, 连接池
db_mysql = PooledMySQLDatabase(
        BACKEND_MYSQL['database'],
        max_connections=BACKEND_MYSQL['max_connections'],
        stale_timeout=BACKEND_MYSQL['stale_timeout'],  # 5 minutes.
        user=BACKEND_MYSQL['user'],
        password=BACKEND_MYSQL['password'],
        host=BACKEND_MYSQL['host'],
        port=BACKEND_MYSQL['port']
)


class BaseModel(Model):
    class Meta:
        database = db_mysql


def create_tmp_data():
    from db.mysql_model.user import User, Profile, Follower
    from db.mysql_model.post import Post, PostReply, PostCategory, PostTopic, CollectPost
    from db.mysql_model.common import Notification
    print("Create TMP Data...")
    db_mysql.create_tables([User, PostCategory, PostTopic, Post, PostReply, CollectPost, Profile, Follower, Notification], safe=True)

    user = User.new(username='admin', nickname='admin', password='admin')
    user.user_profile.nickname = user.nickname
    user_test = User.new(username='root', nickname='root', password='root')
    user_test.user_profile.nickname = user_test.nickname

    # -------------------- 测试关注功能 ---------------
    print('测试关注功能')
    Follower.create(user=user, follower=user_test)

    # -------------------- 测试分类功能 --------------
    print('测试分类功能')
    postcategory0 = PostCategory.create(
        name='学习',
        str='study'
    )
    postcategory1 = PostCategory.create(
        name='娱乐',
        str='entertainment'
    )
    posttopic0 = PostTopic.create(
        name='通知',
        str='notice'
    )
    posttopic1 = PostTopic.create(
        category=postcategory0,
        name='考研资料',
        str='postgraduate'
    )
    posttopic2 = PostTopic.create(
        category=postcategory1,
        name='灌水区',
        str='water'
    )

    # ---------------- 测试新文章 --------------
    print('测试新文章功能')
    post = Post.create(
        topic=posttopic0,
        title='test_vul_scan',
        content="vul_scan_content_04.27_12:47",
        user=user
    )
    post.up_visit()
    post.up_collect()
    Notification.new_post(post, user)

    post_test_0 = Post.create(
        topic=posttopic1,
        title="IDS是一种积极主动的安全防护技术",
        content="入侵检测系统的核心价值在于通过对全网信息的分析，了解信息系统的安全状况，进而指导信息系统安全建设目标以及安全策略的确立和调整，而入侵防御系统的核心价值在于安全策略的实施—对黑客行为的阻击",
            user=user
    )
    Notification.new_post(post_test_0, user)

    post_test_1 = Post.create(
        topic=posttopic2,
        title="IDS是一种积极主动的安全防护技术",
        content='''入侵检测系统的核心价值在于通过对
        全网信息的分析，了解信息系统的安全状况，
        进而指导信息系统安全建设目标以及安全策略的确立和调整，
        而入侵防御系统的核心价值在于安全策略的实施—对黑客行为的阻击''',
        user=user
    )

    Notification.new_post(post_test_1, user)

    # ------------测试新回复--------------
    print('测试新回复功能')
    postreply = PostReply.create(
            post=post,
            user=user,
            content='test_reply'
    )
    postreply.up_like()
    post.update_latest_reply(postreply)

    postreply_test_0 = PostReply.create(
            post=post_test_0,
            user=user,
            content='入侵检测系统需要部署在网络内部，监控范围可以覆盖整个子网，包括来自外部的数据以及内部终端之间传输的数据，入侵防御系统则必须部署在网络边界，抵御来自外部的入侵，对内部攻击行为无能为力。'
    )
    post_test_0.update_latest_reply(postreply_test_0)
    Notification.new_reply(postreply_test_0, post_test_0, user)

    postreply_test_1 = PostReply.create(
        post=post_test_1,
        user=user,
        content='''入侵检测系统需要部署在网络内部，
        监控范围可以覆盖整个子网，
        包括来自外部的数据以及内部终端之间传输的数据，
        入侵防御系统则必须部署在网络边界，抵御来自外部的入侵，对内部攻击行为无能为力。'''
    )
    post_test_1.update_latest_reply(postreply_test_1)
    Notification.new_reply(postreply_test_1, post_test_1, user)


db_init = MySQLDatabase('', user=BACKEND_MYSQL['user'], password=BACKEND_MYSQL['password'], host=BACKEND_MYSQL['host'],
                        port=BACKEND_MYSQL['port'])

if not db_init.execute_sql("select * from information_schema.schemata where schema_name = '{0}'".format(BACKEND_MYSQL['database'])).fetchone():
    db_init.execute_sql("create database {0} default character set utf8 default collate utf8_general_ci".format(BACKEND_MYSQL['database']))
    create_tmp_data()

db_init.close()
