# coding:utf-8
from custor.logger import logger

from db.mysql_model.post import PostCategory, PostTopic, Post
import psutil, datetime, time

# Trick cache
topic_category_cache = {'categorys': [], 'topics': []}
hot_post_cache = {'reply': [], 'visit': []}
system_status_cache = [0, 0, 0, 0]


def update_topic_category_cache():
    """
    update topic
    :return:
    """
    topic_category_cache['categorys'] = []
    topic_category_cache['topics'] = []
    categorys = PostCategory.select()
    for t in range(len(categorys)):
        topic_category_cache['categorys'].append(categorys[t])
        tmp = []
        topics = PostTopic.select().where(PostTopic.category == categorys[t])
        for i in range(len(topics)):
            tmp.append(topics[i])
        topic_category_cache['topics'].append(tmp)
    topics = PostTopic.select().where(PostTopic.category == None)
    tmp = []
    for i in range(len(topics)):
        tmp.append(topics[i])
    topic_category_cache['topics'].append(tmp)


def update_hot_post_cache():
    """
    ignore...
    :return:
    """
    hot_post_cache['reply'] = []
    hot_post_cache['visit'] = []
    posts = Post.select().where(Post.is_delete == False).order_by(Post.reply_count.desc()).limit(4)
    for post in posts:
        hot_post_cache['reply'].append(post)


def update_system_status_cache():
    """
    ignore...
    :return:
    """
    from threading import Thread

    class MonitorWorker(Thread):
        def __init__(self, name, system_status_cache):
            Thread.__init__(self)
            self.name = name
            self.systatus = system_status_cache

        def run(self):
            logger.debug("start monitor system status...")
            while True:
                try:
                    s1 = psutil.cpu_percent()
                    s2 = psutil.virtual_memory()[2]
                    try:
                        s3 = len(psutil.net_connections())
                    except:
                        s3 = 'unkown'
                    s4 = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d")
                    self.systatus[0] = s1
                    self.systatus[1] = s2
                    self.systatus[2] = s3
                    self.systatus[3] = s4
                    from app.api.api import SystemStatusWebsocketHandler
                    SystemStatusWebsocketHandler.write2all(self.systatus)
                    time.sleep(30)
                except KeyboardInterrupt:
                    break

    monitor = MonitorWorker('system', system_status_cache)
    monitor.start()


def update_cache():
    logger.debug('start update cache...')
    update_topic_category_cache()
    update_hot_post_cache()
    update_system_status_cache()

