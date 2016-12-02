# coding:utf-8

class MSGDict(dict):
    """
    rewrite for language
    """
    def __getitem__ (self, key):
        """
        ex: MSG['DB.common.new_post_msg']
        :param key:
        :return:
        """
        keys = key.split('.')
        tmp = self
        for k in keys:
            tmp = super(MSGDict, tmp).__getitem__(k)
        return tmp

MSG = MSGDict({
    'DB': {
        'common': {
            'new_post_msg': '发新文章'
            'new_reply_msg' '发表新评论'
        }
    }
})

