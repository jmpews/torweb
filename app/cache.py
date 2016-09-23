# coding:utf-8
from custor.logger import logger

from db.mysql_model.post import PostCategory, PostTopic, Post

# 缓存一些cache
topic_category_cache = {'categorys': [], 'topics': []}
hot_post_cache = {'reply': [], 'visit': []}
system_status_cache = [0, 0, 0, 0]

def update_topic_category_cache():
    '''
    更新主题分类缓存
    :return:
    '''
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
    '''
    更新 '热门文章' 缓存
    :return:
    '''
    hot_post_cache['reply'] = []
    hot_post_cache['visit'] = []
    posts = Post.select().order_by(Post.reply_count.desc()).limit(4)
    for post in posts:
        hot_post_cache['reply'].append(post)

def update_system_status_cache():
    '''
    系统状态cache
    :return:
    '''
    from threading import Thread

    class MonitorWorker(Thread):
        '''
        监视系统状态线程
        '''
        def __init__(self, name, systatus):
            Thread.__init__(self)
            self.name = name
            self.systatus = systatus
        def run(self):
            logger.debug("start monitor system status...")
            import psutil, datetime, time
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

