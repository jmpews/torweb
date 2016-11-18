# coding:utf8


class Auth:
    authorizations = {
    }

    @staticmethod
    def auth_add_poc(user):
        if user.is_checker():
            return True
        return False
