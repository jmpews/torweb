# coding:utf-8
from custor.utils import get_page_nav, get_page_number
from settings.config import config
from db.mysql_model.post import Post, PostTopic, CollectPost
from db.mysql_model.user import User


def get_index_info(current_page, page_limit=config.default_page_limit):
    current_page = get_page_number(current_page)
    posts, page_number_limit = Post.list_recently(page_number=current_page)
    top_posts, _ = Post.list_top()
    pages = get_page_nav(current_page, page_number_limit, page_limit)
    return posts, top_posts, pages

def get_topic_index_info(topic_id, current_page, page_limit=config.default_page_limit):
    try:
        topic = PostTopic.get(PostTopic.str == topic_id)
    except PostTopic.DoesNotExist:
        return None
    current_page = get_page_number(current_page)
    posts, page_number_limit = Post.list_by_topic(topic, page_number=current_page)
    top_posts, _ = Post.list_top()
    pages = get_page_nav(current_page, page_number_limit, page_limit)
    return topic, posts, top_posts, pages

def get_index_user_info(user):
    posts = Post.select().where(Post.user == user).count()
    collectposts = CollectPost.select().where(CollectPost.user == user).count()
    return {'posts_count': posts, 'collectposts_count': collectposts}