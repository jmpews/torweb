# coding:utf-8
from utils import logger
from db.mysql_model.post import PostCategory, PostTopic, Post

catetopic = {'categorys': [], 'topics': []}
cache_hot_post = {'reply': [], 'visit': []}


def update_catetopic():
    catetopic['categorys'] = []
    catetopic['topics'] = []
    categorys = PostCategory.select()
    for t in range(len(categorys)):
        catetopic['categorys'].append(categorys[t])
        tmp = []
        topics = PostTopic.select().where(PostTopic.category == categorys[t])
        for i in range(len(topics)):
            tmp.append(topics[i])
        catetopic['topics'].append(tmp)
        tmp = []
    topics = PostTopic.select().where(PostTopic.category == None)
    for i in range(len(topics)):
        tmp.append(topics[i])
    catetopic['topics'].append(tmp)

def update_hot_post():
    cache_hot_post['reply'] = []
    cache_hot_post['visit'] = []
    posts = Post.select().order_by(Post.reply_count.desc()).limit(4)
    for post in posts:
        cache_hot_post['reply'].append(post)


def update_cache():
    logger.debug('start update cache...')
    update_catetopic()
    update_hot_post()

