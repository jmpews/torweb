# coding:utf-8
from utils import logger
from backend.mysql_model.post import PostCategory, PostTopic

catetopic = {'categorys': [], 'topics': []}


def update_catetopic():
    categorys = PostCategory.select().limit(10)
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



def update_cache():
    logger.debug('start update cache...')
    update_catetopic()

