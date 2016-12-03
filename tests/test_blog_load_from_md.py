import sys, os
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

from settings.config import config
from peewee import Model, MySQLDatabase

mysqldb = MySQLDatabase('',
                        user=config.BACKEND_MYSQL['user'],
                        password=config.BACKEND_MYSQL['password'],
                        host=config.BACKEND_MYSQL['host'],
                        port=config.BACKEND_MYSQL['port'])


from db.mysql_model.blog import BlogPostCategory, BlogPostLabel, BlogPost
md_path = './docs/articles'


def check_md_format(file_path):
    fd = open(file_path)
    md_info = {}
    while True:
        line = fd.readline().strip()
        if len(line) == 0:
            break
        try:
            i = line.index(':')
            k = line[:i]
            v = line[i+1:]
        except:
            fd.close()
            return None
        md_info[k.strip().lower()] = v.strip()
    # 校验字段是否存在
    # Necessary Args: title, tags
    # Optional Args: date, category, auth, slug
    keys = md_info.keys()
    if 'title' in keys and 'tags' in keys and 'slug' in keys:
        md_info['content'] = fd.read(-1)
        fd.close()
        return md_info
    else:
        fd.close()
        return None


def convert_md_2_post(md_info):
    category = md_info.get('category')
    if not category:
        category = 'UnClassified'
    cate = BlogPostCategory.get_by_name(category)
    post = BlogPost.create(title=md_info['title'],
                           category=cate,
                           slug=md_info['slug'],
                           content=md_info['content'])

    BlogPostLabel.add_post_label(md_info['tags'], post)


def get_files(root_path):
    files = os.listdir(root_path)
    print(files)
    for file_name in files:
        _, suffix = os.path.splitext(file_name)
        if suffix == '.md':
            md_file_path = os.path.join(root_path, file_name)
            md_info = check_md_format(md_file_path)
            if md_info:
                print(md_info['title'])
                convert_md_2_post(md_info)

if __name__ == '__main__':
    mysqldb.create_tables([BlogPostLabel, BlogPost, BlogPostCategory], safe=True)
    t = BlogPostLabel.delete()
    t.execute()
    t = BlogPost.delete()
    t.execute()
    t = BlogPostCategory.delete()
    t.execute()

    get_files(md_path)
