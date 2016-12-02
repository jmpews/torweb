# coding:utf-8

class MSGDict(dict):
    """
    rewrite for language
    """
    def str(self, key):
        """
        ex: MSG.str('DB.common.new_post_msg')
        :param key:
        :return:
        """
        keys = key.split('.')
        tmp = self
        for k in keys:
            tmp = tmp[k]
        return tmp

msg = {
    'DB': {
        'common': {
            'new_post_msg': '发新文章',
            'new_reply_msg': '发表新评论'
        }
    }
}

MSG = MSGDict(msg)

