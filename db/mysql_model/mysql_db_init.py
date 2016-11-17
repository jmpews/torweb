from settings.config import config
from peewee import Model, MySQLDatabase
from custor.logger import logger

mysqldb = MySQLDatabase('',
                        user=config.BACKEND_MYSQL['user'],
                        password=config.BACKEND_MYSQL['password'],
                        host=config.BACKEND_MYSQL['host'],
                        port=config.BACKEND_MYSQL['port'])


def create_test_data(db_mysql):
    from db.mysql_model.user import User, Profile, Follower, ChatLog
    from db.mysql_model.post import Post, PostReply, PostCategory, PostTopic, CollectPost
    from db.mysql_model.common import Notification
    from db.mysql_model.blog import BlogPost, BlogPostLabel, BlogPostCategory

    logger.debug("DataBase is not exist, so create test data.")

    # -------------------- 建表 ---------------
    db_mysql.create_tables([User, ChatLog, PostCategory, PostTopic, Post, PostReply, CollectPost, Profile, Follower, Notification, BlogPostCategory, BlogPost, BlogPostLabel], safe=True)
    user_admin = User.new(username='admin', email='admin@jmp.com', password='admin')
    user_test = User.new(username='test', email='test@jmp.com', password='test')

    # -------------------- 测试关注功能 ---------------
    Follower.create(user=user_admin, follower=user_test)

    # -------------------- 测试分类功能 --------------
    logger.debug("""
    版块分类
    docker:
        docker文章
    registry:
        registry文章、私有hub、images分享, dockerfile分享

    docker集群:
        docker集群文章
    """)

    postcategory0 = PostCategory.create(name='docker', str='docker')
    postcategory1 = PostCategory.create(name='registry', str='registry')
    postcategory2 = PostCategory.create(name='docker集群', str='docker-cluster')

    posttopic0 = PostTopic.create(category=postcategory0, name='docker文章', str='docker-article')

    posttopic1 = PostTopic.create(category=postcategory1, name='registry文章', str='registry-article')
    posttopic2 = PostTopic.create(category=postcategory1, name='私有hub', str='private-hub')
    posttopic3 = PostTopic.create(category=postcategory1, name='image分享', str='image-share')
    posttopic4 = PostTopic.create(category=postcategory1, name='dockerfile分享', str='dockerfile-share')

    posttopic5 = PostTopic.create(category=postcategory2, name='docker集群文章', str='docker-cluster-article')

    posttopic10 = PostTopic.create(name='通知', str='notice')
    posttopic11 = PostTopic.create(name='讨论', str='discussion')


    # ---------------- 测试新文章 --------------
    post = Post.create(
        topic=posttopic0,
        title='test',
        content=tmp_post,
        user=user_admin
    )

    # ---------------- 测试通知 --------------
    Notification.new_post(post)

    # ------------测试新回复--------------
    postreply = PostReply.create(
            post=post,
            user=user_test,
            content='test'
    )
    post.update_latest_reply(postreply)


    # ---------------- 测试Blog --------------
    bpc0 = BlogPostCategory.create(name='Tornado', str='Tornado')
    bp0 = BlogPost.create(title='Tornado', category=bpc0, content='Tornado content')
    BlogPostLabel.add_post_label('python,tornado', bp0)

    # ---------------- 测试chat --------------
    chat_log_0 = ChatLog.create(me=user_admin, other=user_test, content='self>other')
    chat_log_0 = ChatLog.create(me=user_test, other=user_admin, content='other>self')



def mysql_db_init(db_mysql):
    if not mysqldb.execute_sql("select * from information_schema.schemata where schema_name = '{0}';".format(config.BACKEND_MYSQL['database'])).fetchone():
        mysqldb.execute_sql("create database {0} default character set utf8 default collate utf8_general_ci;".format(config.BACKEND_MYSQL['database']))
    else:
        pass
        mysqldb.execute_sql("drop database torweb")
        mysqldb.execute_sql("create database {0} default character set utf8 default collate utf8_general_ci;".format(config.BACKEND_MYSQL['database']))

    create_test_data(db_mysql)
    # logger.debug('load db from db/torweb.sql.')
    # import os
    # os.system(' mysql -u{0} -p{1} {2} <'.format(config.BACKEND_MYSQL['user'], config.BACKEND_MYSQL['password'], config.BACKEND_MYSQL['database'])+os.getcwd()+'/db/torweb.sql')
    mysqldb.close()

import html
tmp_post = """
<pre><code>
"""+html.escape("""
test.test
""")+ """
</code></pre>
"""