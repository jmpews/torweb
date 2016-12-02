# coding:utf-8

MSG = MSGDict({
    'DB': {
        'common': {
            'new_post_msg': '发新文章'
            'new_reply_msg' '发表新评论'
        }
    }
})

class MSGDict(dict):
    def __getitem__ (self, key):
        keys = key.split('.')
        tmp = self
        for k in keys:
            tmp = super(MSGDict, tmp).__getitem__(k)
        return tmp