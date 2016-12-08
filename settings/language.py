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
    },
    'register_same_name': '用户名重复',
    'register_same_email': '用户邮箱重复',
    'login_captcha_error': '验证码错误',
    'login_password_error': '用户名或者密码错误',
}

MSG = MSGDict(msg)

