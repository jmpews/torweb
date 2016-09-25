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

    logger.debug('add user: [admin:admin], [test:test]')
    user_admin = User.new(username='admin', email='admin@jmp.com', password='admin')
    user_test = User.new(username='test', email='test@jmp.com', password='test')

    # -------------------- 测试关注功能 ---------------
    logger.debug('add follower: [test]->[admin]')
    Follower.create(user=user_admin, follower=user_test)

    # -------------------- 测试分类功能 --------------
    logger.debug('add postcategory and posttopic:')
    logger.debug('''
    版块分类
    专业:
        计算机
    学习:
        学习资料、考研资料、家教、竞赛

    生活:
        共享账号、电影资源、常用软件、电脑故障

    爱好:
        摄影、健身

    未分类:
        校园通知、讨论
    ''')

    postcategory0 = PostCategory.create(name='学习', str='study')
    postcategory1 = PostCategory.create(name='专业', str='major')
    postcategory2 = PostCategory.create(name='生活', str='live')
    postcategory3 = PostCategory.create(name='爱好', str='hobby')

    posttopic0 = PostTopic.create(category=postcategory0, name='学习资料', str='study-material')
    posttopic1 = PostTopic.create(category=postcategory0, name='考研资料', str='study-advance-material')
    posttopic2 = PostTopic.create(category=postcategory0, name='竞赛', str='study-competition')
    posttopic3 = PostTopic.create(category=postcategory0, name='请教', str='study-advice')

    posttopic4 = PostTopic.create(category=postcategory1, name='计算机', str='major-computer')

    posttopic5 = PostTopic.create(category=postcategory2, name='电影资源', str='live-movie')
    posttopic6 = PostTopic.create(category=postcategory2, name='共享账号', str='live-account')
    posttopic7 = PostTopic.create(category=postcategory2, name='电脑故障', str='live-computer-repair')

    posttopic8 = PostTopic.create(category=postcategory3, name='摄影', str='hobby-photography')
    posttopic9 = PostTopic.create(category=postcategory3, name='健身', str='hobby-fitness')

    posttopic10 = PostTopic.create(name='通知', str='notice')
    posttopic11 = PostTopic.create(name='讨论', str='discussion')


    # ---------------- 测试新文章 --------------
    logger.debug('add post: [SICP换零钱(递归转尾递归)]')
    post = Post.create(
        topic=posttopic0,
        title='SICP换零钱(递归转尾递归)',
        content=tmp_post,
        user=user_admin
    )

    # ---------------- 测试通知 --------------
    logger.debug('add notice: [admin]->[admin\'s followers]')
    Notification.new_post(post)

    # ------------测试新回复--------------
    logger.debug('add postreply: [test]->[admin]')
    postreply = PostReply.create(
            post=post,
            user=user_test,
            content='迭代需要重复利用递归产生的冗余数据'
    )
    post.update_latest_reply(postreply)


    # ---------------- 测试Blog --------------
    logger.debug('add blogpost: [tornado]')
    bpc0 = BlogPostCategory.create(name='Tornado', str='Tornado')
    bp0 = BlogPost.create(title='Tornado', category=bpc0, content='Tornado content')
    BlogPostLabel.add_post_label('python,tornado', bp0)

    # ---------------- 测试Blog --------------
    logger.debug('add chatlog: [>, <]')
    chat_log_0 = ChatLog.create(me=user_admin, other=user_test, content='self>other')
    chat_log_0 = ChatLog.create(me=user_test, other=user_admin, content='other>self')



def mysql_db_init(db_mysql):
    if not mysqldb.execute_sql("select * from information_schema.schemata where schema_name = '{0}';".format(config.BACKEND_MYSQL['database'])).fetchone():
        mysqldb.execute_sql("create database {0} default character set utf8 default collate utf8_general_ci;".format(config.BACKEND_MYSQL['database']))
    else:
        mysqldb.execute_sql("drop database torweb")
        mysqldb.execute_sql("create database {0} default character set utf8 default collate utf8_general_ci;".format(config.BACKEND_MYSQL['database']))

    create_test_data(db_mysql)
    # logger.debug('load db from db/torweb.sql.')
    # import os
    # os.system(' mysql -u{0} -p{1} {2} <'.format(config.BACKEND_MYSQL['user'], config.BACKEND_MYSQL['password'], config.BACKEND_MYSQL['database'])+os.getcwd()+'/db/torweb.sql')
    mysqldb.close()

import html
tmp_post = '''
<pre><code>
'''+html.escape('''
/*
 * =====================================================================================
 *
 *  Filename:  p26.c
 *
 *  Description: change money
 *
 *  Version:  1.0
 *  Created:  2016/08/02 14时58分22秒
 *  Revision:  none
 *  Compiler:  gcc
 *
 *  Author:  jmpews (jmpews.github.io), jmpews@gmail.com
 *
 * =====================================================================================
 */


#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int count_change(int amount);
int cc(int amount, int kinds_of_coins);
void count_iter(int *tmp, int t, int amount);
int get_coin(int index_of_coin);
int get_index_tmp(int index_of_coin);
int *get_tmp_array(int kinds_of_coins);
int get_recycle_value(int index_of_coin, int current_amount, int *tmp_array);
void update_recycle_value(int index_of_coin, int *tmp_array, int value);

int main ( int argc, char *argv[] )
{
    int t;
    t = count_change(100);
    printf("%d", t);
    return EXIT_SUCCESS;
}               /* ----------  end of function main  ---------- */

int count_change(int amount) {
    cc(amount, 5);
    return 0;
}

int cc(int amount, int kinds_of_coins) {
    int *tmp = get_tmp_array(kinds_of_coins);
    int t = 0;
    tmp[0] = 0;
    count_iter(tmp, t, amount);
    return 0;
}

// 这里这里也是关键点，这个尾递归的结束由t(当前需要兑换的金钱)和amount(需要兑换的目标金钱)控制，为线性，也就是说时间复杂度为O(n)
void count_iter(int *tmp, int t, int amount) {
    int r;
    r = get_recycle_value(1, t, tmp);
    update_recycle_value(1, tmp, r);

    //C2(t) = C2(t-get_coin(2)) + C1(t)
    r = get_recycle_value(2, t, tmp) + r;
    update_recycle_value(2, tmp, r);

    //C3(t) = C3(t-get_coin(3)) + C2(t)
    r = get_recycle_value(3, t, tmp) + r;
    update_recycle_value(3, tmp, r);

    //C4(t) = C4(t-get_coin(4)) + C3(t)
    r= get_recycle_value(4, t, tmp) + r;
    update_recycle_value(4, tmp, r);

    //C5(t) = C5(t-get_coin(5)) + C4(t)
    r = get_recycle_value(5, t, tmp) + r;
    if(t == amount) {
        printf("final-value: %d\n", r);
        exit(1);
    }
    update_recycle_value(5, tmp, r);

    count_iter(tmp, t+1, amount);
}

int get_coin(int index_of_coin) {
    switch(index_of_coin) {
        case 1: return 1;
        case 2: return 5;
        case 3: return 10;
        case 4: return 25;
        case 5: return 50;
        default: exit(1);
    }
}

// 对于C1、C2、C3、C4、C5缓存队列开始的位置
int get_index_tmp(int index_of_coin) {
    switch(index_of_coin) {
        case 1: return 0;
        case 2: return 1;
        case 3: return 6;
        case 4: return 16;
        case 5: return 41;
        default: exit(1);
    }
}

// 分配固定的缓存, 无论需要兑换多少金钱，只要金币种类不变，缓存的大小就是固定的。 空间复杂度为常量。
// "因为它的状态能由其中的三个状态变量完全刻画，解释器在执行 这一计算过程时，只需要保存这三个变量的轨迹就足够了" 这句话在这里就有体现了
int *get_tmp_array(int kinds_of_coins) {
    int *tmp;
    int i;
    int sum = 0;
    for(i=1 ; i<kinds_of_coins ; i++) {
        sum += get_coin(i);
    }
    tmp = (int *)malloc(sizeof(int) * sum);
    memset(tmp, 0 ,sizeof(int) * sum);
    return tmp;
}

// 获取重复利用值, 每次缓存队列头的位置
// 比如: 此时缓存队列为[C2(0), C2(1), C2(2), C2(3), C2(4)]
// C2(5) = C1(5) + C2(0) 此时我们需要取缓存队列头的值C2(0)
// 计算完得到C2(5)，需要执行update_recycle_value将得到C2(5)进队列，除去旧的C2(0)，此时队列头尾C2(1)，即为计算C2(6)需要的缓存值
int get_recycle_value(int index_of_coin, int current_amount, int *tmp_array) {
    int t = get_index_tmp(index_of_coin);
    if(current_amount < get_coin(index_of_coin)){
        return 0;
    }
    else if(current_amount == get_coin(index_of_coin)){
        return 1;
    }
    else {
        return tmp_array[t];
    }
}

// 更新重复利用值(队列的概念), 计算出最新的值，需要替换旧的利用值
// 比如: C2(5) = C1(5) + C2(0)
// 现在C2缓存队列中有[C2(0), C2(1), C2(2), C2(3), C2(4)]，我们需要将C2(5)进队列，[C2(1), C2(2), C2(3), C2(4), C2(5)]
void update_recycle_value(int index_of_coin, int *tmp_array, int value) {
    int i;
    int t = get_index_tmp(index_of_coin);
    for(i = 0; i< (get_coin(index_of_coin)-1); i++) {
        tmp_array[t+i] = tmp_array[t+i+1];
    }
    tmp_array[t+get_coin(index_of_coin)-1] = value;
}
''')+ '''
</code></pre>
'''